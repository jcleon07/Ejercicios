def  counting_sort(A, exp):
    n = len(A)

    out = [0]*n

    count = [0]*10

    for i in range(n):
        index = A[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i-1]

    i = n-1
    while i >= 0:
        index = A[i] // exp
        out[count[index % 10] - 1] = A[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        A[i] = out[i]