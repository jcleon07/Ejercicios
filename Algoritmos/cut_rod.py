#RECURSIVE TOP-DOWN
def cut_rod(p, n):
    if n == 0:
        return 0
    
    q = float('-inf')

    for i in range(1, n):
        q = max(q, p[i] + cut_rod(p, n-i))

    return q