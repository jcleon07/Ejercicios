import numpy as np

# ------------------------ INPUTS ---------------------------

#Elefir modo (cifrado o descifrado)
mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().strip()

if (mode != "CIFRAR" and mode != "DESCIFRAR"):
    print("Solo se acepta CIFRAR o DESCIFRAR, vuelva a digitar corrrectamente")
    exit()

#Mensaje a cifrar/descifrar
msg = list(input("Ingrese el mensaje sin tildes: ").upper().replace(" ",""))
for i in range(len(msg)):
    if msg[i] == "J":
        msg[i] = "I"
    if msg[i] == "Ñ":
        msg[i] = "N"

index = 0
while index < len(msg) - 1:
    if msg[index] == msg[index+1]: 
        msg.insert(index+1, "X")
    index += 2

if len(msg) % 2 != 0:
    msg.append("X")

#Keyword matriz 5x5
key = []
print("Introduzca la llave (matriz 5x5): \n")
for i in range(5):
    row = input(f"Introduzca la fila separando los elementos con espacio {i+1}: ").upper().split()

    if len(row) != 5: 
        print("La fila debe ser de 5 elementos")
        exit()

    row = ["I" if letra == "J" else letra for letra in row]
    key.append(row)
key = np.array(key)

if len(set(key.flatten())) != 25: 
    print("Matriz construida con elementos repetidos, vuelva a intentar...\n")
    exit()

#Verifica que cada elemento de la matriz sea exactamente una letra
for i in range(5):
    for j in range(5):
        if len(key[i][j]) != 1 or not key[i][j].isalpha():
            print("\nIngrese la matriz con solo una letra por indice (use 'I' para la celda I/J)... ")
            exit()


# ------------------------ CIFRADO ---------------------------

if mode == "CIFRAR":

    for i in range(0, len(msg), 2):
        row_a, col_a = np.where(key == msg[i])
        row_b, col_b = np.where(key == msg[i+1])

        row_a, col_a = int(row_a[0]), int(col_a[0])
        row_b, col_b = int(row_b[0]), int(col_b[0])

        if row_a == row_b:
            msg[i] = str(key[row_a][(col_a+1) % 5])
            msg[i+1] = str(key[row_b][(col_b+1) % 5])

        elif col_a == col_b:
            msg[i] = str(key[(row_a+1) % 5][col_a])
            msg[i+1] = str(key[(row_b+1) % 5][col_b])

        else:
            msg[i] = str(key[row_a][col_b])
            msg[i+1] = str(key[row_b][col_a])

    print("Mensaje cifrado: " + "".join(msg))

# ------------------------ DESCIFRADO ---------------------------

elif mode =="DESCIFRAR":

    for i in range(0, len(msg), 2):
        row_a, col_a = np.where(key == msg[i])
        row_b, col_b = np.where(key == msg[i+1])

        row_a, col_a = int(row_a[0]), int(col_a[0])
        row_b, col_b = int(row_b[0]), int(col_b[0])

        if row_a == row_b:
            msg[i] = str(key[row_a][(col_a-1) % 5])
            msg[i+1] = str(key[row_b][(col_b-1) % 5])

        elif col_a == col_b:
            msg[i] = str(key[(row_a-1) % 5][col_a])
            msg[i+1] = str(key[(row_b-1) % 5][col_b])

        else:
            msg[i] = str(key[row_a][col_b])
            msg[i+1] = str(key[row_b][col_a])

    print("Mensaje descifrado: " + "".join(msg))

else:
    print("Expresion incorrecta")
    exit()