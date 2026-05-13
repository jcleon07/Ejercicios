def insertion_sort(A, n):
    for i in range(1, n):
        key = A[i]
        j = i-1
        while j >= 0 and A[j] > key:
            A[j+1] = A[j]
            j = j-1
        A[j+1] = key
    return A

def bucket_sort(A):
    n = len(A)
    B = [[] for _ in range(n)]

    for i in A:
        bi = int(n*i)
        B[bi].append(i)

    for i in B:
        insertion_sort(i, len(i))
    
    index = 0
    for i in B:
        for j in i:
            A[index] = j
            index += 1


A = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
bucket_sort(A)

print(A)






