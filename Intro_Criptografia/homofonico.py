import random
import unicodedata

# ------------------------- LIMPIEZA DE TEXTO ------------------------

def limpiar(texto):

    texto = unicodedata.normalize("NFD", texto.upper())
    return "".join(c for c in texto if "A" <= c <= "Z")

# ------------------------- LAYOUT (m = 100, n = 26) ------------------------

layout = {
    "A": [9, 12, 33, 47, 53, 67, 78, 92],
    "B": [48, 81],
    "C": [13, 41, 62],
    "D": [1, 3, 45, 79],
    "E": [14, 16, 24, 44, 46, 55, 57, 64, 74, 82, 87, 98],
    "F": [10, 31],
    "G": [6, 25],
    "H": [23, 39, 50, 56, 65, 68],
    "I": [32, 70, 73, 83, 88, 93],
    "J": [15],
    "K": [4],
    "L": [26, 37, 51, 84],
    "M": [22, 27],
    "N": [18, 58, 59, 66, 71, 91],
    "O": [0, 5, 7, 54, 72, 90, 99],
    "P": [38, 95],
    "Q": [94],
    "R": [29, 35, 40, 42, 77, 80],
    "S": [11, 19, 36, 76, 86, 96],
    "T": [17, 20, 30, 43, 49, 69, 75, 85, 97],
    "U": [8, 61, 63],
    "V": [34],
    "W": [60, 89],
    "X": [28],
    "Y": [21, 52],
    "Z": [2],
}

inverso = {num: letra for letra, nums in layout.items() for num in nums}

# ------------------------- INPUTS ------------------------

mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().replace(" ", "")
if mode not in ["CIFRAR","DESCIFRAR"]:
    print("Ingrese CIFRAR o DESCIFRAR, no se acepta otro tipo de cadena...\n")
    exit()

if mode == "CIFRAR":
    msg = limpiar(input(f"Ingrese el mensaje a {mode}: "))
    if not msg:
        print("El mensaje no contiene letras validas...\n")
        exit()
else:
    msg = input(f"Ingrese el mensaje a {mode} (numeros de 00 a 99 separados por espacio): ").replace(",", " ").split()
    if len(msg) == 1 and len(msg[0]) > 2:
        if len(msg[0]) % 2 != 0:
            print("Si los numeros van pegados, cada uno debe tener exactamente dos digitos (longitud par)...\n")
            exit()
        msg = [msg[0][i:i+2] for i in range(0, len(msg[0]), 2)]
    if not msg:
        print("El mensaje no contiene numeros validos...\n")
        exit()


# ------------------------- CIFRADO ------------------------

if mode == "CIFRAR":
    cifrado = [f"{random.choice(layout[c]):02d}" for c in msg]

    print(f"Mensaje cifrado: {' '.join(cifrado)}")


# ------------------------- DESCIFRADO ------------------------

elif mode == "DESCIFRAR":
    descifrado = []
    for token in msg:
        if not (token.isascii() and token.isdigit()) or int(token) not in inverso:
            print(f"'{token}' no es un numero valido del layout (00 - 99)...\n")
            exit()
        descifrado.append(inverso[int(token)])

    print(f"Mensaje descifrado: {''.join(descifrado)}")
