import numpy as np
import unicodedata
from math import gcd


# ------------------------- LIMPIEZA DE TEXTO ------------------------

def limpiar(texto):

    texto = unicodedata.normalize("NFD", texto.upper())
    return "".join(c for c in texto if "A" <= c <= "Z")

# ------------------------- FUNCIONES ------------------------

def a_numeros(texto):
    return [ord(c) - ord("A") for c in texto]

def a_texto(numeros):
    return "".join(chr(int(n) + ord("A")) for n in numeros)

def determinante(m):
    return int(m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0]) % 26

def inversa_modular(m):
    det = determinante(m)
    det_inv = pow(det, -1, 26)
    adj = np.array([[ m[1, 1], -m[0, 1]],
                    [-m[1, 0],  m[0, 0]]], dtype=int)
    return (det_inv * adj) % 26

# ------------------------- INPUTS ------------------------

mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().replace(" ", "")
if mode not in ["CIFRAR","DESCIFRAR"]:
    print("Ingrese CIFRAR o DESCIFRAR, no se acepta otro tipo de cadena...\n")
    exit()

key = np.zeros((2, 2), dtype=int)
for i in range(2):
    fila = [int(x) for x in input(f"Introduzca la fila {i+1} (dos enteros separados por espacio): ").split()]
    if len(fila) != 2:
        print("Cada fila debe tener exactamente dos numeros...\n")
        exit()

    key[i, 0] = fila[0] % 26
    key[i, 1] = fila[1] % 26

det = determinante(key)
if det == 0 or gcd(det, 26) != 1:
    print(f"La matriz no es invertible modulo 26 (det = {det}, gcd(det, 26) = {gcd(det, 26)})...\n")
    exit()

msg = limpiar(input(f"Ingrese el mensaje a {mode}: "))
if not msg:
    print("El mensaje no contiene letras validas...\n")
    exit()


# ------------------------- CIFRADO ------------------------

if mode == "CIFRAR":
    if len(msg) % 2 != 0:
        msg += "X"

    numeros = a_numeros(msg)
    cifrado = []
    for i in range(0, len(numeros), 2):
        bloque = np.array(numeros[i:i+2], dtype=int)
        cifrado.extend((key @ bloque) % 26)

    print(f"Mensaje cifrado: {a_texto(cifrado)}")


# ------------------------- DESCIFRADO ------------------------

elif mode == "DESCIFRAR":
    if len(msg) % 2 != 0:
        print("El mensaje cifrado debe tener longitud par...\n")
        exit()

    key_inv = inversa_modular(key)
    numeros = a_numeros(msg)
    descifrado = []
    for i in range(0, len(numeros), 2):
        bloque = np.array(numeros[i:i+2], dtype=int)
        descifrado.extend((key_inv @ bloque) % 26)

    print(f"Mensaje descifrado: {a_texto(descifrado)}")
