#RECURSIVE TOP-DOWN
def cut_rod(p, n):
    if n == 0:
        return 0
    
    q = float('-inf')

    for i in range(1, n):
        q = max(q, p[i] + cut_rod(p, n-i))

    return q

def memoized_cut_rod_aux(p, n, r):
    if r[n] >= 0:
        return r[n]

    if n == 0:
        q = 0
    else:
        q = float('-inf')

        for i in range(1,n):
            q = max(q, p[i] + memoized_cut_rod_aux(p,n-i,r))

    r[n] = q
    return q 

def memoized_cut_rod(p, n):
    r = [0]*n

    for i in range(n):
        r[i] = float('-inf')

    return memoized_cut_rod_aux(p, n, r)


#BOTTOM UP IMPL
def bottom_up_cut_rod(p, n):
    r = [0]*n
    r[0] = 0

    for j in range(1, n):
        q = float('-inf')

        for i in range(1, j):
            q = max(q, p[i] + r[j-i])

        r[j] = q
        return r[n]


def extended_bottom_up_cut_rod(p, n):
    r = [0]*n
    s = [0]*n

    r[0] = 0

    for j in range(1, n):
        q = float('-inf')

        for i in range(1, j):

            if q < p[i] + r[j-i]:
                q = p[i] + r[j-i]
                s[j] = i

        r[j] = q

    return r, s

def print_cot_rod_solution(p, n):
    r,s = extended_bottom_up_cut_rod(p, n)

    while n > 0:
        print(s[n])
        n = n - s[n]