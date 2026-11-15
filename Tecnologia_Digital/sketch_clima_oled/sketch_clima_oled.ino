#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --- Configuration ---
const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// Open-Meteo (free, no API key). Bogota: lat 4.711, lon -74.0721
const char* weatherUrl =
  "http://api.open-meteo.com/v1/forecast?latitude=4.711&longitude=-74.0721"
  "&current=temperature_2m,relative_humidity_2m,weather_code,is_day"
  "&timezone=America%2FBogota";

const uint32_t UPDATE_INTERVAL_MS = 10UL * 60UL * 1000UL; // Refresh every 10 min
const uint32_t RETRY_INTERVAL_MS  = 30UL * 1000UL;        // Retry after an error

// --- OLED Display Configuration (same as Ej_OLED / voltmeter) ---
#define I2C_SDA 8
#define I2C_SCL 9
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// --- Team logo: arrow ">" + smile, 16x12 px (1 bit per pixel, MSB = left) ---
const uint16_t TEAM_LOGO[12] = {
  0xE000, 0x7000, 0x3800, 0x1C00, 0x0E00, 0x1C00,
  0x3800, 0x7000, 0xE303, 0x0387, 0x01FE, 0x00FC
};

// --- Shared data between tasks (protected by a mutex) ---
struct WeatherData {
  float temperature;
  int   humidity;
  int   code;        // WMO weather code
  bool  isDay;
  char  updated[6];  // "HH:MM" from the API
  bool  valid;
};

enum NetState { CONNECTING_WIFI, FETCHING, DATA_OK, FETCH_ERROR };

WeatherData g_weather = {0, 0, 0, true, "--:--", false};
volatile NetState g_netState = CONNECTING_WIFI;
SemaphoreHandle_t xWeatherMutex;

// --- Task Prototypes ---
void taskWeather(void *pvParameters);
void taskDisplay(void *pvParameters);

// =============================================================================
// DRAWING HELPERS
// =============================================================================
void drawTeamLogo(int16_t x, int16_t y, uint8_t scale) {
  for (uint8_t r = 0; r < 12; r++) {
    for (uint8_t c = 0; c < 16; c++) {
      if (TEAM_LOGO[r] & (0x8000 >> c)) {
        display.fillRect(x + c * scale, y + r * scale, scale, scale, SSD1306_WHITE);
      }
    }
  }
}

void drawSun(int16_t cx, int16_t cy, int16_t r) {
  display.fillCircle(cx, cy, r, SSD1306_WHITE);
  for (int i = 0; i < 8; i++) {
    float a = i * PI / 4.0;
    display.drawLine(cx + cos(a) * (r + 3), cy + sin(a) * (r + 3),
                     cx + cos(a) * (r + 7), cy + sin(a) * (r + 7), SSD1306_WHITE);
  }
}

void drawMoon(int16_t cx, int16_t cy, int16_t r) {
  display.fillCircle(cx, cy, r, SSD1306_WHITE);
  display.fillCircle(cx + r / 2 + 1, cy - r / 3, r - 1, SSD1306_BLACK);
}

// Outlined cloud (white border, black inside) so it can cover a sun/moon or another cloud.
// Occupies roughly x+2..x+38, y-2..y+20
void drawCloud(int16_t x, int16_t y) {
  display.fillCircle(x + 10, y + 12, 8, SSD1306_WHITE);
  display.fillCircle(x + 20, y + 8, 10, SSD1306_WHITE);
  display.fillCircle(x + 30, y + 12, 8, SSD1306_WHITE);
  display.fillRect(x + 10, y + 12, 20, 9, SSD1306_WHITE);

  display.fillCircle(x + 10, y + 12, 6, SSD1306_BLACK);
  display.fillCircle(x + 20, y + 8, 8, SSD1306_BLACK);
  display.fillCircle(x + 30, y + 12, 6, SSD1306_BLACK);
  display.fillRect(x + 10, y + 12, 20, 7, SSD1306_BLACK);
}

void drawRain() {
  for (int i = 0; i < 4; i++) {
    int x = 10 + i * 8;
    display.drawLine(x + 4, 47, x, 57, SSD1306_WHITE);
    display.drawLine(x + 5, 47, x + 1, 57, SSD1306_WHITE);
  }
}

void drawDrizzle() {
  for (int i = 0; i < 4; i++) {
    int x = 12 + i * 8;
    display.drawFastVLine(x, 47, 3, SSD1306_WHITE);
    display.drawFastVLine(x - 2, 54, 3, SSD1306_WHITE);
  }
}

void drawSnow() {
  for (int i = 0; i < 3; i++) {
    int x = 12 + i * 10;
    int y = (i % 2 == 0) ? 51 : 57;
    display.drawLine(x - 2, y, x + 2, y, SSD1306_WHITE);
    display.drawLine(x, y - 2, x, y + 2, SSD1306_WHITE);
    display.drawLine(x - 2, y - 2, x + 2, y + 2, SSD1306_WHITE);
    display.drawLine(x - 2, y + 2, x + 2, y - 2, SSD1306_WHITE);
  }
}

void drawLightning() {
  display.fillTriangle(25, 45, 17, 55, 26, 52, SSD1306_WHITE);
  display.fillTriangle(21, 52, 29, 52, 18, 63, SSD1306_WHITE);
}

// Draws the weather icon in the left area (x 0..47, y 15..63)
void drawWeatherIcon(int code, bool isDay) {
  if (code == 0) {                                  // Clear sky
    if (isDay) drawSun(24, 39, 9);
    else       drawMoon(24, 39, 10);
  } else if (code == 1 || code == 2) {              // Mainly clear / partly cloudy
    if (isDay) drawSun(30, 27, 6);
    else       drawMoon(30, 27, 7);
    drawCloud(2, 34);
  } else if (code == 3) {                           // Overcast
    drawCloud(8, 22);
    drawCloud(2, 34);
  } else if (code == 45 || code == 48) {            // Fog
    drawCloud(4, 20);
    display.drawFastHLine(6, 47, 34, SSD1306_WHITE);
    display.drawFastHLine(10, 52, 30, SSD1306_WHITE);
    display.drawFastHLine(6, 57, 34, SSD1306_WHITE);
  } else if (code >= 51 && code <= 57) {            // Drizzle
    drawCloud(4, 22);
    drawDrizzle();
  } else if ((code >= 61 && code <= 67) || (code >= 80 && code <= 82)) { // Rain / showers
    drawCloud(4, 22);
    drawRain();
  } else if ((code >= 71 && code <= 77) || code == 85 || code == 86) {   // Snow
    drawCloud(4, 22);
    drawSnow();
  } else if (code >= 95) {                          // Thunderstorm
    drawCloud(4, 20);
    drawLightning();
  } else {                                          // Unknown code
    drawCloud(4, 28);
  }
}

// Short Spanish description (max ~13 chars to fit the right column)
const char* weatherText(int code) {
  if (code == 0)                return "Despejado";
  if (code == 1)                return "Poco nublado";
  if (code == 2)                return "Parc. nublado";
  if (code == 3)                return "Nublado";
  if (code == 45 || code == 48) return "Niebla";
  if (code >= 51 && code <= 57) return "Llovizna";
  if (code >= 61 && code <= 67) return "Lluvia";
  if (code >= 71 && code <= 77) return "Nieve";
  if (code >= 80 && code <= 82) return "Chubascos";
  if (code == 85 || code == 86) return "Nieve";
  if (code >= 95)               return "Tormenta";
  return "Desconocido";
}

// =============================================================================
// JSON HELPERS (simple search, no extra library needed)
// =============================================================================
float jsonNumber(const String& json, const char* key, int from) {
  String k = String("\"") + key + "\":";
  int i = json.indexOf(k, from);
  if (i < 0) return NAN;
  return json.substring(i + k.length()).toFloat();
}

bool fetchWeather() {
  HTTPClient http;
  http.begin(weatherUrl);
  int httpCode = http.GET();

  if (httpCode != HTTP_CODE_OK) {
    Serial.printf("[Weather] HTTP error: %d\n", httpCode);
    http.end();
    return false;
  }

  String body = http.getString();
  http.end();

  // Search only inside the "current":{...} object (skip "current_units")
  int start = body.indexOf("\"current\":{");
  if (start < 0) {
    Serial.println("[Weather] Unexpected JSON");
    return false;
  }

  float temp = jsonNumber(body, "temperature_2m", start);
  float hum  = jsonNumber(body, "relative_humidity_2m", start);
  float code = jsonNumber(body, "weather_code", start);
  float day  = jsonNumber(body, "is_day", start);
  if (isnan(temp) || isnan(code)) return false;

  // "time":"2026-11-15T14:30"  ->  "14:30"
  char hhmm[6] = "--:--";
  int t = body.indexOf("\"time\":\"", start);
  if (t >= 0) {
    int tPos = body.indexOf('T', t + 8);
    if (tPos > 0) body.substring(tPos + 1, tPos + 6).toCharArray(hhmm, sizeof(hhmm));
  }

  if (xSemaphoreTake(xWeatherMutex, portMAX_DELAY) == pdTRUE) {
    g_weather.temperature = temp;
    g_weather.humidity    = isnan(hum) ? 0 : (int)hum;
    g_weather.code        = (int)code;
    g_weather.isDay       = (day != 0);
    strncpy(g_weather.updated, hhmm, sizeof(g_weather.updated));
    g_weather.valid       = true;
    xSemaphoreGive(xWeatherMutex);
  }

  Serial.printf("[Weather] %.1f C | Hum %d%% | code %d (%s) | %s | %s\n",
                temp, (int)hum, (int)code, weatherText((int)code),
                day != 0 ? "dia" : "noche", hhmm);
  return true;
}

// =============================================================================
// SETUP / LOOP
// =============================================================================
void setup() {
  Serial.begin(115200);

  Wire.begin(I2C_SDA, I2C_SCL);
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Error: SSD1306 OLED display not detected"));
    for (;;);
  }
  display.cp437(true);   // Correct CP437 table for á, é and the degree symbol
  display.setTextColor(SSD1306_WHITE);
  display.clearDisplay();
  display.display();

  xWeatherMutex = xSemaphoreCreateMutex();

  // Weather task (network), Core 1
  xTaskCreatePinnedToCore(taskWeather, "WeatherTask", 8192, NULL, 2, NULL, 1);
  // Display task (OLED), Core 0
  xTaskCreatePinnedToCore(taskDisplay, "DisplayTask", 4096, NULL, 1, NULL, 0);
}

void loop() {
  vTaskDelete(NULL);
}

// =============================================================================
// TASK 1: WIFI + WEATHER DOWNLOAD
// =============================================================================
void taskWeather(void *pvParameters) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  for (;;) {
    // (Re)connect Wi-Fi if needed
    if (WiFi.status() != WL_CONNECTED) {
      g_netState = CONNECTING_WIFI;
      Serial.print("[Weather] Connecting Wi-Fi");
      while (WiFi.status() != WL_CONNECTED) {
        vTaskDelay(pdMS_TO_TICKS(500));
        Serial.print(".");
      }
      Serial.println("\n[Weather] WiFi Connected.");
    }

    g_netState = FETCHING;
    if (fetchWeather()) {
      g_netState = DATA_OK;
      vTaskDelay(pdMS_TO_TICKS(UPDATE_INTERVAL_MS));
    } else {
      g_netState = FETCH_ERROR;
      vTaskDelay(pdMS_TO_TICKS(RETRY_INTERVAL_MS));
    }
  }
}

// =============================================================================
// TASK 2: OLED USER INTERFACE
// =============================================================================
void taskDisplay(void *pvParameters) {
  WeatherData local;
  char buffer[24];
  uint8_t dots = 0;

  for (;;) {
    if (xSemaphoreTake(xWeatherMutex, pdMS_TO_TICKS(10)) == pdTRUE) {
      local = g_weather;
      xSemaphoreGive(xWeatherMutex);
    }

    display.clearDisplay();

    // Header: team logo + title
    drawTeamLogo(0, 0, 1);
    display.setTextSize(1);
    display.setCursor(22, 2);
    display.print("Clima Bogot\xA0");
    // Small status mark at the right of the header
    display.setCursor(116, 2);
    if (g_netState == FETCHING)          display.print("..");
    else if (g_netState == FETCH_ERROR)  display.print("!");
    else if (g_netState == CONNECTING_WIFI) display.print("W");
    display.drawFastHLine(0, 13, SCREEN_WIDTH, SSD1306_WHITE);

    if (local.valid) {
      // Left: weather icon
      drawWeatherIcon(local.code, local.isDay);

      // Right column: temperature with degree symbol
      display.setTextSize(2);
      display.setCursor(50, 17);
      display.print(local.temperature, 1);
      int16_t x = display.getCursorX();
      display.setTextSize(1);
      display.setCursor(x + 1, 17);
      display.print("\xF8");
      display.setTextSize(2);
      display.setCursor(x + 8, 17);
      display.print("C");

      // Description, humidity and last update
      display.setTextSize(1);
      display.setCursor(50, 37);
      display.print(weatherText(local.code));

      snprintf(buffer, sizeof(buffer), "Humedad %d%%", local.humidity);
      display.setCursor(50, 47);
      display.print(buffer);

      snprintf(buffer, sizeof(buffer), "Act. %s", local.updated);
      display.setCursor(50, 57);
      display.print(buffer);
    } else {
      // No data yet: status screen
      display.setTextSize(1);
      display.setCursor(4, 28);
      if (g_netState == CONNECTING_WIFI)  display.print("Conectando WiFi...");
      else if (g_netState == FETCH_ERROR) display.print("Error, reintentando");
      else                                display.print("Consultando clima...");

      dots = (dots + 1) % 4;
      for (uint8_t i = 0; i < dots; i++) {
        display.fillCircle(52 + i * 12, 48, 3, SSD1306_WHITE);
      }
    }

    display.display();
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}
