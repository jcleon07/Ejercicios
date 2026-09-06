import serial
import serial.tools.list_ports


def listar_puertos():
    """Muestra los puertos disponibles para ayudar a elegir el correcto."""
    puertos = serial.tools.list_ports.comports()
    print("Puertos disponibles:")
    for p in puertos:
        print(f" - {p.device}: {p.description}")
    print()


listar_puertos()

puerto = input("Ingresa el puerto del ESP32 (ej: COM3 o /dev/ttyUSB0): ")
baudrate = 115200
try:
    ser = serial.Serial(puerto, baudrate, timeout=1)
    print(f"\nConectado a {puerto} a {baudrate} baudios")
    print("Esperando datos del ESP32... (Ctrl+C para salir)\n")

    while True:
        linea = ser.readline().decode('utf-8', errors='ignore').strip()
        if linea:
            print(f"[ESP32] {linea}")

except serial.SerialException as e:
    print(f"Error al abrir el puerto: {e}")

except KeyboardInterrupt:
    print("\nMonitor detenido por el usuario.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()


