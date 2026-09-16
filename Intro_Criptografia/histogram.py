import matplotlib.pyplot as mp

frecuency = {chr(i): 0 for i in range(ord('A'), ord('Z') + 1)}

#Introducir nombre del archivo
with open("", "r", encoding="latin-1") as archivo:          
    raw = archivo.read()

    raw = raw.replace(" ", "").replace("\n", "")

    for character in raw.upper():
        if character in frecuency:
            frecuency[character] += 1

    for character, count in frecuency.items():
        print(character, count)

    letras = list(frecuency.keys())
    valores = list(frecuency.values())

    mp.figure(figsize=(12, 6))
    mp.bar(letras, valores, color="skyblue", edgecolor="black")
    mp.title("Frecuencia de letras en el texto")
    mp.xlabel("Letra")
    mp.ylabel("Frecuencia")
    mp.tight_layout()
    mp.show()

    