from copy import deepcopy

def get_multiples_indices(l, start, stop, base_index, cache={}):
    if l[base_index] in cache.keys():
        if base_index in cache[l[base_index]]:
            while base_index != cache[l[base_index]].pop(0):
                # cache[l[base_index]].remove(base_index)
                pass
            return cache[l[base_index]]
    mult_indices = []
    for i in range(start, stop):
        if l[i] % l[base_index] == 0:
            mult_indices.append(i)
    cache[l[base_index]] = deepcopy(mult_indices)
    print("cache: {}".format(cache))
    return mult_indices

def count_lucky_triples(l):
    total = 0
    cache = {}
    for i in range(len(l)):
        mid_indices = get_multiples_indices(l, i+1, len(l), i, cache)
        for j in mid_indices:
            temp =  get_multiples_indices(l, j+1, len(l), j, cache) 
            total += len(temp)
            print("j:{} , total: {}, temp: {}".format(j,total, temp))
    return total


def solution(l):
    return count_lucky_triples(l)
