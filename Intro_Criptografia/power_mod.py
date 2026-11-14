def power_mod(a, b, n):
    if n == 1:
        return 0
    
    z = 1
    b_bits = bin(b)[2:]
    for bit in b_bits:
        if bit == "1": 
            z = ((z**2)*a) % n
        else:
            z = (z**2) % n
    
    return z



a = int(input("Introduzca a: "))
b = int(input("Introduzca b: "))
n = int(input("Introduzca n: "))

res = power_mod(a, b, n)

print("\nEl resultado es: ", res)

