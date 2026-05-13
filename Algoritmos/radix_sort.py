import counting_sort as cs

def radix_sort(A, d):
    exp = 1
    for i in range(d):
        cs.counting_sort(A, exp)
        exp *= 10


A = [170, 45, 75, 90, 802, 24, 2, 66]
radix_sort(A, 3)

print(A)