import numpy as np
import unicodedata

# ------------------------- LIMPIEZA DE TEXTO ------------------------

def limpiar(texto):
    
    texto = unicodedata.normalize("NFD", texto.upper())
    return "".join(c for c in texto if "A" <= c <= "Z")

# ------------------------- INPUTS ------------------------

mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().replace(" ", "")
if mode not in ["CIFRAR","DESCIFRAR"]:
    print("Ingrese CIFRAR o DESCIFRAR, no se acepta otro tipo de cadena...\n")
    exit()

key = limpiar(input("Ingrese la llave: "))
if len(key) == 0:
    print("La llave debe contener al menos una letra...\n")
    exit()

try:
    t = int(input("Ingrese la cantidad de letras que tiene cada bloque de strings (parametro t): "))
except ValueError:
    print("El parametro t debe ser un numero entero...\n")
    exit()
if t <= 0:
    print("El parametro t debe ser mayor que 0...\n")
    exit()

msg = limpiar(input(f"Ingrese el mensaje a {mode}: "))

# ------------------------- MATRIZ DE VIGENERE ------------------------

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
matrix = [[0 for i in range(26)] for i in range(26)]
n = range(len(matrix))

index = 0
for row in n:
    for j in n:
        pos = (index + j) % 26
        matrix[row][j] = abc[pos]

    index += 1
matrix = np.array(matrix)  

res = ""

# ------------------------- CIFRADO ------------------------

if mode == "CIFRAR":
    for i in range(len(msg)):
        k = key[i % len(key)]

        row_key = ord(k) - ord('A')
        col_msg = ord(msg[i]) - ord('A')

        cifred = matrix[row_key, col_msg]

        if (i+1) % t == 0:
            res += cifred + " "
        else:
            res += cifred

    print("El mensaje cifrado es: ", res.strip())

# ------------------------- DESCIFRADO ------------------------

elif mode == "DESCIFRAR":
    for i in range(len(msg)):
        k = key[i % len(key)]

        row_key = ord(k) - ord('A')
        col_msg = np.where(matrix[row_key, :] == msg[i])[0][0]

        orig = matrix[0, col_msg]
        res += orig

    print("El mensaje descifrado es: ", res)
