import math
 
def hash_multiplicacion(k, A, M):

    producto = k * A
    fraccionaria = producto - math.floor(producto)  # frac(k * A)
    return math.floor(M * fraccionaria)
 
def main():
    K = int(input())
    A = float(input())
    M = int(input())
 
    for _ in range(K):
        k = int(input())
        print(hash_multiplicacion(k, A, M))
 
if __name__ == "__main__":
    main()
 