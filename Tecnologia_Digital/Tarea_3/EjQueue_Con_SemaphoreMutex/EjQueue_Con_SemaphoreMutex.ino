#include <Arduino.h>

// Define a structured data type to pass
struct SensorData {
  int id;
  float temperature;
};

// Variables globales compartidas: reemplazan el buffer interno de la queue.
// sharedData guarda la última lectura y newDataAvailable indica si hay un dato sin leer.
SensorData sharedData;
bool newDataAvailable = false;

// Mutex que protege el acceso a las variables compartidas (reemplaza a dataQueue)
SemaphoreHandle_t dataMutex;

// Task Function Declarations
void SenderTask(void *pvParameters);
void ReceiverTask(void *pvParameters);

void setup() {
  Serial.begin(115200);

  // Wait for Serial to initialize (good practice on ESP32-S3 USB-CDC natively)
  delay(1000);
  Serial.println("Initializing system...");

  // Se crea el mutex en lugar de xQueueCreate
  dataMutex = xSemaphoreCreateMutex();

  if (dataMutex != NULL) {
    Serial.println("Mutex created successfully.");

    // Pinning SenderTask to Core 1, Priority 1
    xTaskCreatePinnedToCore(
      SenderTask,       // Task function
      "Sender",         // Task name text
      3000,             // Stack size (in words)
      NULL,             // Parameter passed to task
      1,                // Priority (Lower)
      NULL,             // Task handle
      1                 // Core ID: 1 (APP_CPU)
    );

    // Pinning ReceiverTask to Core 1, Priority 2 (Higher priority than sender)
    xTaskCreatePinnedToCore(
      ReceiverTask,     // Task function
      "Receiver",       // Task name text
      3000,             // Stack size (in words)
      NULL,             // Parameter passed to task
      2,                // Priority (Higher)
      NULL,             // Task handle
      1                 // Core ID: 1 (APP_CPU)
    );
  } else {
    Serial.println("Error creating the mutex!");
  }
}

void SenderTask(void *pvParameters) {
  // Print the core this task is currently running on to verify configuration
  Serial.printf("SenderTask started on Core %d\n", xPortGetCoreID());

  SensorData currentReadings = {1, 24.5};

  while(1) {
    currentReadings.temperature += 0.1; // Simulate sensor update

    // Equivalente a xQueueSend: se toma el mutex (esperando hasta 10 ticks)
    // antes de escribir en la variable global.
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(10)) == pdTRUE) {
      if (!newDataAvailable) {
        sharedData = currentReadings;
        newDataAvailable = true;
        Serial.println("[Sender] Data written to shared variable");
      } else {
        // El dato anterior no se ha leído: equivale a "queue llena" (capacidad 1)
        Serial.println("[Sender] Previous data not read yet, data discarded");
      }
      xSemaphoreGive(dataMutex); // Libera el mutex para el Receiver
    } else {
      Serial.println("[Sender] Mutex busy, data discarded");
    }

    // Delay for 1000ms (Yields CPU to other tasks)
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void ReceiverTask(void *pvParameters) {
  // Print the core this task is currently running on to verify configuration
  Serial.printf("ReceiverTask started on Core %d\n", xPortGetCoreID());

  SensorData receivedData;
  bool hasData;

  while(1) {
    hasData = false;

    // Equivalente a xQueueReceive: se toma el mutex, se copia el dato a una
    // variable local y se marca como leído.
    if (xSemaphoreTake(dataMutex, portMAX_DELAY) == pdTRUE) {
      if (newDataAvailable) {
        receivedData = sharedData;
        newDataAvailable = false;
        hasData = true;
      }
      xSemaphoreGive(dataMutex);
    }

    // Se imprime fuera de la sección crítica para no retener el mutex
    if (hasData) {
      Serial.printf("[Receiver] Received ID: %d, Temp: %.2f (Core %d)\n",
                    receivedData.id,
                    receivedData.temperature,
                    xPortGetCoreID());
    }

    // Sin queue la tarea no se bloquea esperando datos, así que consulta
    // periódicamente. El delay evita que, por tener mayor prioridad, acapare la CPU.
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void loop() {
  // The main Arduino loop runs on Core 1 at Priority 1.
  // We leave it empty so it doesn't starve our custom tasks.
  vTaskDelete(NULL);
}
