def is_prime(num):

    count = 0
    for i in range(1, num):
        if num % i == 0:
            count += 1

    if count < 2:
        return 1
    else:
        return 0

num = int(input("Ingrese un numero entero: "))

primes = 0
for i in range(2, num):
    primes += is_prime(i)

print(f"Hay {primes} numeros primos antes de {num}")