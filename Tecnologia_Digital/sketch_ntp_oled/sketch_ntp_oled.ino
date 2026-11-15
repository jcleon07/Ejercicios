#include <WiFi.h>
#include "time.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --- Configuration ---
const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// Time settings: GMT-5, No DST
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -5 * 3600; // -18000 seconds
const int   daylightOffset_sec = 0;    // No daylight saving time

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

void drawTeamLogo(int16_t x, int16_t y, uint8_t scale) {
  for (uint8_t r = 0; r < 12; r++) {
    for (uint8_t c = 0; c < 16; c++) {
      if (TEAM_LOGO[r] & (0x8000 >> c)) {
        display.fillRect(x + c * scale, y + r * scale, scale, scale, SSD1306_WHITE);
      }
    }
  }
}

// --- Sync state shared between tasks (only the Display task touches the OLED) ---
enum SyncState { CONNECTING_WIFI, WAITING_NTP, SYNCED };
volatile SyncState g_syncState = CONNECTING_WIFI;

// --- FreeRTOS Task Handles ---
TaskHandle_t syncTaskHandle = NULL;

// --- Task Prototypes ---
void taskSyncTime(void *pvParameters);
void taskDisplayTime(void *pvParameters);

// Prints a text horizontally centered at row y
void printCentered(const char* text, int16_t y) {
  int16_t x1, y1;
  uint16_t w, h;
  display.getTextBounds(text, 0, y, &x1, &y1, &w, &h);
  display.setCursor((SCREEN_WIDTH - w) / 2, y);
  display.print(text);
}

void setup() {
  Serial.begin(115200);

  // Initialize the I2C bus with the ESP32-S3 pins and the OLED
  Wire.begin(I2C_SDA, I2C_SCL);
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Error: SSD1306 OLED display not detected"));
    for (;;);
  }
  display.cp437(true);   // Use the correct CP437 table so á and é render properly
  display.setTextColor(SSD1306_WHITE);
  display.clearDisplay();
  display.display();

  // 1. Create Synchronization Task (Higher priority, Core 1)
  xTaskCreatePinnedToCore(
    taskSyncTime,      // Function
    "SyncTimeTask",    // Name
    4096,              // Stack size
    NULL,              // Parameters
    2,                 // Priority
    &syncTaskHandle,   // Handle (assigned here)
    1                  // Core
  );

  // 2. Create Display Task (Lower priority, Core 0)
  xTaskCreatePinnedToCore(
    taskDisplayTime,
    "DisplayTimeTask",
    4096,
    NULL,
    1,
    NULL,
    0
  );
}

void loop() {
  // FreeRTOS handles everything. The loop task can be deleted.
  vTaskDelete(NULL);
}

// --- TASK: CONNECT WIFI & SYNC NTP ---
void taskSyncTime(void *pvParameters) {
  Serial.println("[Sync] Starting Wi-Fi connection...");
  g_syncState = CONNECTING_WIFI;
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    vTaskDelay(500 / portTICK_PERIOD_MS);
    Serial.print(".");
  }
  Serial.println("\n[Sync] WiFi Connected.");

  // Configure the ESP32 internal system time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("[Sync] Synchronizing with NTP server...");
  g_syncState = WAITING_NTP;

  struct tm timeinfo;
  // Wait until time is actually retrieved from the network
  while (!getLocalTime(&timeinfo)) {
    vTaskDelay(1000 / portTICK_PERIOD_MS);
    Serial.println("[Sync] Waiting for NTP response...");
  }

  Serial.println("[Sync] System Time Synchronized!");
  g_syncState = SYNCED;

  // Disconnect WiFi to save power after sync
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  Serial.println("[Sync] WiFi turned off.");

  // SUSPEND TASK: The task enters a suspended state.
  Serial.println("[Sync] Task Suspending now...");
  vTaskSuspend(NULL);

  // This part of the code is never reached while suspended
  for (;;) { vTaskDelay(1000); }
}

// --- TASK: DISPLAY TIME IN SPANISH (OLED + Serial) ---
void taskDisplayTime(void *pvParameters) {
  struct tm timeinfo;
  char buffer[32];

  // Spanish Arrays (CP437 codes: \x82 = é, \xA0 = á; split strings so the hex escape ends there)
  const char* dias[] = {"Domingo", "Lunes", "Martes", "Mi\x82" "rcoles", "Jueves", "Viernes", "S\xA0" "bado"};
  const char* meses[] = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
  // Plain versions for the Serial Monitor (UTF-8)
  const char* diasSerial[] = {"Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"};

  for (;;) {
    display.clearDisplay();

    // Short timeout (10 ms) so the task does not block 5 s while the clock is not set
    if (getLocalTime(&timeinfo, 10)) {
      // Serial output (same as before)
      Serial.printf("Fecha: %s, %02d de %s de %04d | Hora: %02d:%02d:%02d\n",
                    diasSerial[timeinfo.tm_wday],
                    timeinfo.tm_mday,
                    meses[timeinfo.tm_mon],
                    timeinfo.tm_year + 1900,
                    timeinfo.tm_hour,
                    timeinfo.tm_min,
                    timeinfo.tm_sec);

      // Day of the week
      display.setTextSize(1);
      printCentered(dias[timeinfo.tm_wday], 2);

      // Date: "14 de Noviembre 2026"
      snprintf(buffer, sizeof(buffer), "%d de %s %04d",
               timeinfo.tm_mday, meses[timeinfo.tm_mon], timeinfo.tm_year + 1900);
      printCentered(buffer, 13);

      display.drawFastHLine(0, 24, SCREEN_WIDTH, SSD1306_WHITE);

      // Time: "HH:MM:SS" in large font
      display.setTextSize(2);
      snprintf(buffer, sizeof(buffer), "%02d:%02d:%02d",
               timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
      printCentered(buffer, 31);

      // Footer: team logo on the left + status text
      display.drawFastHLine(0, 50, SCREEN_WIDTH, SSD1306_WHITE);
      drawTeamLogo(2, 52, 1);
      display.setTextSize(1);
      display.setCursor(30, 54);
      display.print("GMT-5 | NTP OK");
    } else {
      // Status screen while the clock is not set yet
      display.setTextSize(1);
      drawTeamLogo(2, 2, 1);
      printCentered("RELOJ NTP", 4);
      display.drawFastHLine(0, 15, SCREEN_WIDTH, SSD1306_WHITE);

      if (g_syncState == CONNECTING_WIFI) {
        printCentered("Conectando WiFi...", 28);
      } else {
        printCentered("Sincronizando NTP...", 28);
      }

      // Simple animated dots so you can tell it is alive
      static uint8_t dots = 0;
      dots = (dots + 1) % 4;
      for (uint8_t i = 0; i < dots; i++) {
        display.fillCircle(52 + i * 12, 48, 3, SSD1306_WHITE);
      }

      Serial.println("[Display] Waiting for system clock to be set...");
    }

    display.display();

    // Refresh display every 1 second
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}
