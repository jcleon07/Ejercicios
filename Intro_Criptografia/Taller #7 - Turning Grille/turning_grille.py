import numpy as np
import unicodedata

# ------------------------- LIMPIEZA DE TEXTO ------------------------

def limpiar(texto):

    texto = unicodedata.normalize("NFD", texto.upper())
    return "".join(c for c in texto if "A" <= c <= "Z")

# ------------------------- FUNCIONES ------------------------

def rotar(hoyos, n, direccion):
    if direccion == 1:
        return [(c, n - 1 - f) for f, c in hoyos]
    return [(n - 1 - c, f) for f, c in hoyos]

def orden_de_posiciones(hoyos, n, direccion):
    posiciones = []
    actuales = list(hoyos)
    for _ in range(4):
        for celda in sorted(actuales):
            if celda not in posiciones:
                posiciones.append(celda)
        actuales = rotar(actuales, n, direccion)
    return posiciones

def mostrar_matriz(matriz):
    for fila in matriz:
        print("    " + " ".join(fila))

# ------------------------- INPUTS ------------------------

try:
    n = int(input("Introduzca el tamano de la reticula (ej. 4 para 4x4): "))
except ValueError:
    print("El tamano debe ser un numero entero...\n")
    exit()
if n < 2:
    print("El tamano de la reticula debe ser mayor o igual a 2...\n")
    exit()

direccion = input("Introduzca la direccion de rotacion (1 = horario, 0 = antihorario): ").strip()
if direccion not in ["0", "1"]:
    print("La direccion solo puede ser 1 (horario) o 0 (antihorario)...\n")
    exit()
direccion = int(direccion)

mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().replace(" ", "")
if mode not in ["CIFRAR","DESCIFRAR"]:
    print("Ingrese CIFRAR o DESCIFRAR, no se acepta otro tipo de cadena...\n")
    exit()

esperados = (n * n) // 4 + (n % 2)
try:
    cantidad = int(input(f"Introduzca la cantidad de hoyos (para {n}x{n} deben ser {esperados}): "))
except ValueError:
    print("La cantidad de hoyos debe ser un numero entero...\n")
    exit()
if cantidad != esperados:
    print(f"Una reticula de {n}x{n} necesita exactamente {esperados} hoyos...\n")
    exit()

hoyos = []
for i in range(cantidad):
    try:
        celda = [int(x) for x in input(f"Introduzca el hoyo {i+1} (fila y columna de 1 a {n}, separadas por espacio): ").replace(",", " ").split()]
    except ValueError:
        print("La fila y la columna deben ser numeros enteros...\n")
        exit()
    if len(celda) != 2 or not (1 <= celda[0] <= n and 1 <= celda[1] <= n):
        print(f"Cada hoyo debe ser una fila y una columna entre 1 y {n}...\n")
        exit()
    if (celda[0] - 1, celda[1] - 1) in hoyos:
        print("Ese hoyo ya fue ingresado...\n")
        exit()
    hoyos.append((celda[0] - 1, celda[1] - 1))

# ------------------------- VALIDACION DE LA REJILLA ------------------------

centro = (n // 2, n // 2) if n % 2 != 0 else None
if centro is not None and centro not in hoyos:
    print(f"En una reticula impar la celda central ({n//2 + 1}, {n//2 + 1}) debe ser un hoyo...\n")
    exit()

cubiertas = []
actuales = list(hoyos)
for _ in range(4):
    cubiertas.extend(c for c in actuales if c != centro)
    actuales = rotar(actuales, n, direccion)

if len(cubiertas) != len(set(cubiertas)):
    print("Rejilla invalida: al rotar, dos hoyos caen sobre la misma celda...\n")
    exit()

posiciones = orden_de_posiciones(hoyos, n, direccion)

print("\nRejilla (O = hoyo):")
rejilla = np.full((n, n), ".")
for f, c in hoyos:
    rejilla[f, c] = "O"
mostrar_matriz(rejilla)

msg = limpiar(input(f"\nIngrese el mensaje a {mode}: "))
if not msg:
    print("El mensaje no contiene letras validas...\n")
    exit()

bloque = n * n


# ------------------------- CIFRADO ------------------------

if mode == "CIFRAR":
    if len(msg) % bloque != 0:
        msg += "X" * (bloque - len(msg) % bloque)

    cifrado = ""
    for b in range(0, len(msg), bloque):
        matriz = np.full((n, n), " ")
        for k, (f, c) in enumerate(posiciones):
            matriz[f, c] = msg[b + k]

        print(f"\nBloque {b // bloque + 1}:")
        mostrar_matriz(matriz)
        cifrado += "".join(matriz.flatten())

    print(f"\nMensaje cifrado: {cifrado}")


# ------------------------- DESCIFRADO ------------------------

elif mode == "DESCIFRAR":
    if len(msg) % bloque != 0:
        print(f"La longitud del mensaje cifrado debe ser multiplo de {bloque}...\n")
        exit()

    descifrado = ""
    for b in range(0, len(msg), bloque):
        matriz = np.array(list(msg[b:b + bloque])).reshape(n, n)

        print(f"\nBloque {b // bloque + 1}:")
        mostrar_matriz(matriz)
        descifrado += "".join(matriz[f, c] for f, c in posiciones)

    print(f"\nMensaje descifrado: {descifrado}")
