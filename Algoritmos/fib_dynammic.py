def fib(n, M):
    if n == 0 or n == 1:
        return M[n]
    if M[n] == -1:
        if M[n-1] == -1:
            M[n-1] = fib(n-1, M)
        if M[n-2] == -1:
            M[n-2] = fib(n-2, M)

        M[n] = M[n-1] + M[n-2]
    
    return M[n]

#BOTTOM UP APPROACH
def fib_bottom_up(n):
    M = [0]*n
    M[1] = 1

    for i in range(2, n):
        M[i] = M[i-1] + M[i-2]
    
    return M[n]

