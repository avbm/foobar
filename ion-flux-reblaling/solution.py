from math import log

def get_parent(num, height, cache={}):
    n = int(log(num,2))
    if num == 2**height - 1:
        return -1
    elif num == 2**(n+1) - 1:
        return 2**(n+2) - 1
    elif num in range(2**(n+1)-n-1, 2**(n+1) - 1 ):
        return num + 1
    else:
        if num in cache.keys():
            return num
        cache[num] = get_parent( num - (2**n - 1), height) + 2**n -1
        return cache[num]

def solution(h, q):
    soln = []
    for i in q:
        soln.append(get_parent(i, h))
    return soln
