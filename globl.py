from numpy import empty, uint8
from math import factorial

def perms(n):
    f = 1
    p = empty((2*n-1, factorial(n)), uint8)
    for i in range(n):
        p[i, :f] = i
        p[i+1:2*i+1, :f] = p[:i, :f]
        for j in range(i):
            p[:i+1, f*(j+1):f*(j+2)] = p[j+1:j+i+2, :f]
        f = f*(i+1)
    return p[:n, :]

#def globl(G):
