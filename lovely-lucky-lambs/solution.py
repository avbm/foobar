from math import log


def next_fibo(count = 0, last2 = (1,1)):
    if count < 2:
        return 1, count+1, last2
    num = last2[0] + last2[1]
    last2 = (last2[1], num)
    return (num, count+1, last2)

def stingy_solution(total_lambs):
    sum = 0
    count = 0
    last2= (1,1)
    while sum < total_lambs:
        num, count, last2 = next_fibo(count, last2) 
        sum += num
    if sum == total_lambs:
        return count
    else:
        return count -1

def generous_solution(total_lambs):
    return int(log(total_lambs+1, 2))

def solution(total_lambs):
    return stingy_solution(total_lambs) - generous_solution(total_lambs)


