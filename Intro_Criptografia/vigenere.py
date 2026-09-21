import numpy as np

mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().replace(" ", "")
if mode not in ["CIFRAR","DESCIFRAR"]:
    print("Ingrese CIFRAR o DESCIFRAR, no se acepta otro tipo de cadena...\n")
    exit()

key = input("Ingrese la llave: ").upper().replace(" ", "")

t = int(input("Ingrese la cantidad de letras que tiene cada bloque de strings (parametro t): "))

msg = input(f"Ingrese el mensaje a {mode}: ").upper()


abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
matrix = [[0 for i in range(26)] for i in range(26)]
n = range(len(matrix))
index = 0


for row in n:
    for j in n:
        pos = (index + j) % 26
        matrix[row][j] = abc[pos]

    index += 1



if mode == "CIFRAR":
    for i in range(msg):
        row_key, col_key = np.where(matrix == )
        row_msg, col_msg = np.where(matrix == )

        row_key, col_key = int(row_key[0]), int(col_key[0])
        row_msg, col_msg = int(row_msg[0]), int(col_msg[0])


elif mode == "DESCIFRAR":
    for i in range(msg):
        row_key, col_key = np.where(matrix == )
        row_msg, col_msg = np.where(matrix == )

        row_key, col_key = int(row_key[0]), int(col_key[0])
        row_msg, col_msg = int(row_msg[0]), int(col_msg[0])

else:
    print("Modo inexistente... ")
    exit()