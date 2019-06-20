def get_multiples_indices(l, start, stop, base_index):
    mult_indices = []
    for i in range(start, stop):
        if l[i] % l[base_index] == 0:
            mult_indices.append(i)
    return mult_indices

def count_lucky_triples(l):
    sum = 0
    for i in range(len(l)):
        mid_indices = get_multiples_indices(l, i+1, len(l), i)
        for j in mid_indices:
            sum += len( get_multiples_indices(l, j+1, len(l), j))
    return sum


def solution(l):
    return count_lucky_triples(l)

