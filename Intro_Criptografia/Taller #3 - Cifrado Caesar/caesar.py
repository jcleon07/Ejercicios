# ------------------------ INPUTS -------------------------

mode = input("Introduzca CIFRAR o DESCIFRAR segun desee: ").upper().replace(" ", "")

if mode not in ["CIFRAR","DESCIFRAR"]:
    print("Ingrese un modo de uso adecuado (CIFRAR o DESCIFRAR)...\n")    
    exit()

text = input("Introduzca el texto: ").upper().replace(" ", "")

k = int(input("Introduzca la cantidad de espacios a mover: ").replace(" ",""))
k = k % 26

ans = ""


# ------------------------ ENCRIPTAR -------------------------

if mode == "CIFRAR":

    for i in range(len(text)):
        letter = ord(text[i])
        if letter < 65 or letter > 90:
            continue
        else:
            num = letter + k

        if num > 90:
            num -= 26
        if (i+1) % 5 == 0:
            ans += chr(num) + " "
        else:
            ans += chr(num) 

# ------------------------ DESENCRIPTAR -------------------------

elif mode == "DESCIFRAR":

    for i in range(len(text)):
        letter = ord(text[i])
        if letter < 65 or letter > 90:
            continue
        else:
            num = letter - k

        if num < 65:
            num += 26
        ans += chr(num)

# ------------------------ MANEJO DE ERROR -------------------------

else:
    print("ERROR...")
    exit()

# ------------------------ IMPRIMIR RESULTADO -------------------------
print(ans)
