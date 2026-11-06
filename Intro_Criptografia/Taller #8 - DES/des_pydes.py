import os
import base64
import numpy as np
from PIL import Image
from pyDes import des, CBC, PAD_PKCS5

# ------------------------- CLAVE ------------------------

CLAVE = b"UNAL2026"
IV = b"CRIPTO26"

# ------------------------- CONVERSION BYTES <-> BITS ------------------------

def bytes_a_bits(datos):
    return np.unpackbits(np.frombuffer(datos, dtype=np.uint8))

def bits_a_bytes(bits):
    return np.packbits(bits).tobytes()

def mostrar_bits(bits, n=64):
    return "".join(map(str, bits[:n]))

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

# ------------------------- IMAGEN A BITS ------------------------

bits = bytes_a_bits(datos)
print(f"\nImagen leida: {len(datos)} bytes -> {len(bits)} bits")
print(f"Primeros 64 bits de la imagen:   {mostrar_bits(bits)}")

cifrador = des(CLAVE, CBC, IV, pad=None, padmode=PAD_PKCS5)
print(f"\nClave DES: {CLAVE.decode()}  ({mostrar_bits(bytes_a_bits(CLAVE))})")
print(f"Vector de inicializacion (CBC): {IV.decode()}")

# ------------------------- CIFRADO ------------------------

print("\nCifrando con DES (puede tardar unos segundos)...")
cifrado_bits = bytes_a_bits(cifrador.encrypt(bits_a_bytes(bits)))
print(f"\nPrimeros 64 bits cifrados:       {mostrar_bits(cifrado_bits)}")

texto_b64 = base64.b64encode(bits_a_bytes(cifrado_bits)).decode()
print("\nTexto cifrado en Base64:\n")
print(texto_b64)
print(f"\nLongitud del texto Base64: {len(texto_b64)} caracteres")

# ------------------------- DESCIFRADO ------------------------

bits_recuperados = bytes_a_bits(base64.b64decode(texto_b64))
print(f"\nBase64 decodificado a {len(bits_recuperados)} bits")

print("Descifrando con DES (puede tardar unos segundos)...")
descifrado_bits = bytes_a_bits(cifrador.decrypt(bits_a_bytes(bits_recuperados)))
print(f"Primeros 64 bits descifrados:    {mostrar_bits(descifrado_bits)}")

datos_descifrados = bits_a_bytes(descifrado_bits)
nombre, extension = os.path.splitext(ruta)
salida = f"{nombre}_descifrada_pydes{extension}"
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
