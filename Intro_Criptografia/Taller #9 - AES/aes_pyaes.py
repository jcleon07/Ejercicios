import os
import base64
import numpy as np
from PIL import Image
import pyaes

# ------------------------- CLAVES ------------------------

CLAVES = {
    128: b"UNAL2026Cripto16",
    192: b"UNAL2026CriptoAES192bits",
    256: b"UNAL2026CriptografiaAES256bits!!",
}
IV = b"CRIPTO2026IV16by"

# ------------------------- CONVERSION BYTES <-> BITS ------------------------

def bytes_a_bits(datos):
    return np.unpackbits(np.frombuffer(datos, dtype=np.uint8))

def bits_a_bytes(bits):
    return np.packbits(bits).tobytes()

def mostrar_bits(bits, n=64):
    return "".join(map(str, bits[:n]))

# ------------------------- AES ------------------------

def cifrar_aes(datos, clave):
    cifrador = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(clave, iv=IV))
    return cifrador.feed(datos) + cifrador.feed()

def descifrar_aes(datos, clave):
    descifrador = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(clave, iv=IV))
    return descifrador.feed(datos) + descifrador.feed()

# ------------------------- INPUTS ------------------------

ruta = input("Introduzca la ruta de la imagen: ").strip().strip('"')
if not os.path.isfile(ruta):
    print("No se encontro el archivo indicado...\n")
    exit()

with open(ruta, "rb") as f:
    datos = f.read()

if not datos:
    print("El archivo esta vacio...\n")
    exit()

try:
    nivel = int(input("Introduzca el nivel de seguridad de AES (128, 192 o 256): ").strip())
except ValueError:
    print("El nivel de seguridad debe ser 128, 192 o 256...\n")
    exit()
if nivel not in CLAVES:
    print("El nivel de seguridad debe ser 128, 192 o 256...\n")
    exit()

clave = CLAVES[nivel]

# ------------------------- IMAGEN A BITS ------------------------

bits = bytes_a_bits(datos)
print(f"\nImagen leida: {len(datos)} bytes -> {len(bits)} bits")
print(f"Primeros 64 bits de la imagen:   {mostrar_bits(bits)}")

print(f"\nNivel de seguridad: AES-{nivel}")
print(f"Clave AES: {clave.decode()}  ({len(clave) * 8} bits)")
print(f"Vector de inicializacion (CBC): {IV.decode()}")

# ------------------------- CIFRADO ------------------------

print(f"\nCifrando con AES-{nivel} (puede tardar unos segundos)...")
cifrado_bits = bytes_a_bits(cifrar_aes(bits_a_bytes(bits), clave))
print(f"\nPrimeros 64 bits cifrados:       {mostrar_bits(cifrado_bits)}")

texto_b64 = base64.b64encode(bits_a_bytes(cifrado_bits)).decode()
print("\nTexto cifrado en Base64:\n")
print(texto_b64)
print(f"\nLongitud del texto Base64: {len(texto_b64)} caracteres")

# ------------------------- DESCIFRADO ------------------------

bits_recuperados = bytes_a_bits(base64.b64decode(texto_b64))
print(f"\nBase64 decodificado a {len(bits_recuperados)} bits")

print(f"Descifrando con AES-{nivel} (puede tardar unos segundos)...")
descifrado_bits = bytes_a_bits(descifrar_aes(bits_a_bytes(bits_recuperados), clave))
print(f"Primeros 64 bits descifrados:    {mostrar_bits(descifrado_bits)}")

datos_descifrados = bits_a_bytes(descifrado_bits)
nombre, extension = os.path.splitext(ruta)
salida = f"{nombre}_descifrada_aes{nivel}{extension}"
with open(salida, "wb") as f:
    f.write(datos_descifrados)

print(f"\nImagen descifrada guardada en: {salida}")
if datos_descifrados == datos:
    print("La imagen descifrada es identica a la original.")
else:
    print("La imagen descifrada NO coincide con la original.")

# ------------------------- MOSTRAR IMAGEN ------------------------

try:
    Image.open(salida).show()
except Exception:
    print("No se pudo abrir la imagen con PIL, abrala manualmente desde la ruta indicada.")
