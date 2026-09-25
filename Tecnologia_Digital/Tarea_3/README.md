# EjQueue con Semáforo Mutex

Versión del ejemplo `EjQueue.ino` (clase del 14 de septiembre) en la que la comunicación entre tareas **no usa queues**. En su lugar se usan **variables globales protegidas por un semáforo mutex** de FreeRTOS. El programa está pensado para un ESP32 (p. ej. ESP32-S3) con el framework de Arduino.

## ¿Qué hace el programa?

Hay dos tareas de FreeRTOS, ambas en el Core 1:

- **SenderTask** (prioridad 1): simula un sensor que cada segundo aumenta la temperatura en 0.1 °C y publica la lectura.
- **ReceiverTask** (prioridad 2): recoge la lectura publicada y la imprime por el monitor serial.

El resultado en consola es el mismo que el del ejemplo original: una lectura nueva por segundo con su ID y temperatura.

## Qué se añadió y cómo reemplaza a la queue

| Con queue (original) | Con mutex (esta versión) |
|---|---|
| `QueueHandle_t dataQueue` | `SemaphoreHandle_t dataMutex` |
| Buffer interno de la queue (10 elementos) | Variable global `SensorData sharedData` (1 elemento) |
| La queue sabe si tiene datos | Bandera global `bool newDataAvailable` |
| `xQueueCreate(10, sizeof(SensorData))` | `xSemaphoreCreateMutex()` |
| `xQueueSend(...)` | `xSemaphoreTake` → escribir `sharedData` y poner la bandera en `true` → `xSemaphoreGive` |
| `xQueueReceive(..., portMAX_DELAY)` | `xSemaphoreTake` → copiar `sharedData` si la bandera está en `true` y ponerla en `false` → `xSemaphoreGive` |

### Elementos añadidos

- **`sharedData`**: variable global donde el Sender deja la última lectura. Cumple el papel del espacio de almacenamiento que antes tenía la queue.
- **`newDataAvailable`**: bandera que indica si hay un dato que el Receiver todavía no ha leído. Evita que el Receiver imprima el mismo dato dos veces y permite al Sender saber si el “buffer” está ocupado.
- **`dataMutex`**: mutex que garantiza que solo una tarea a la vez lea o escriba `sharedData` y `newDataAvailable`. Sin él, el Receiver podría leer la estructura a medio escribir (por ejemplo, el `id` nuevo con la `temperature` vieja). Una queue hace esta protección de forma interna; aquí se hace explícitamente.

### Diferencias de comportamiento frente a la queue

1. **Capacidad de 1 dato.** La queue original podía guardar hasta 10 lecturas; aquí solo hay una variable. Si el Sender quiere escribir y el dato anterior no se ha leído, el dato nuevo se descarta (equivale a “queue llena”).
2. **Consulta periódica (polling).** `xQueueReceive` con `portMAX_DELAY` bloqueaba al Receiver hasta que llegaba un dato. Un mutex solo protege el acceso, no avisa de datos nuevos, por eso el Receiver revisa la bandera cada 100 ms con `vTaskDelay`. Ese delay es necesario: el Receiver tiene mayor prioridad y, sin él, nunca soltaría la CPU y el Sender no podría ejecutarse.
3. **Sección crítica corta.** El Receiver copia el dato a una variable local dentro del mutex y hace el `Serial.printf` afuera, para no retener el mutex mientras imprime.

## Funciones

### `setup()`
Inicializa el puerto serial a 115200 baudios, crea el mutex con `xSemaphoreCreateMutex()` y, si se creó correctamente, lanza las dos tareas con `xTaskCreatePinnedToCore` en el Core 1 (Sender con prioridad 1 y Receiver con prioridad 2). Si el mutex no se pudo crear, imprime un error y no crea las tareas.

### `SenderTask(void *pvParameters)`
Tarea productora. Imprime en qué core se ejecuta y arranca con la lectura `{id = 1, temperature = 24.5}`. En cada ciclo:
1. Incrementa la temperatura en 0.1.
2. Intenta tomar el mutex esperando como máximo 10 ticks.
3. Si el dato anterior ya fue leído, copia la lectura en `sharedData` y pone `newDataAvailable = true`; si no, descarta la lectura.
4. Libera el mutex y espera 1000 ms.

### `ReceiverTask(void *pvParameters)`
Tarea consumidora. Imprime en qué core se ejecuta. En cada ciclo:
1. Toma el mutex (espera indefinida).
2. Si `newDataAvailable` es `true`, copia `sharedData` a una variable local y pone la bandera en `false`.
3. Libera el mutex.
4. Si obtuvo un dato, imprime ID, temperatura y core.
5. Espera 100 ms antes de volver a consultar.

### `loop()`
No se usa. Llama a `vTaskDelete(NULL)` para eliminar la tarea del loop de Arduino y dejar la CPU a las tareas propias.

## Uso

Abrir el `.ino` en el Arduino IDE (el IDE puede pedir moverlo a una carpeta con su mismo nombre), seleccionar la placa ESP32 correspondiente, cargar y abrir el Monitor Serial a **115200** baudios.
