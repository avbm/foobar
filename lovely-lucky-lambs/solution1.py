from math import log

#CURRENT_FIBO = [1, 1]

def next_fibo(current_fibo = []):
    if len(current_fibo) < 2:
        current_fibo.append(1)
        return 1
    num = current_fibo[-1] + current_fibo[-2]
    current_fibo.append(num)
    #print(current_fibo)
    return num

def stingy_solution(total_lambs):
    sum = 0
    current_fibo = []
    while sum < total_lambs:
        sum += next_fibo(current_fibo)
    #print(sum)
    #print(current_fibo)
    if sum == total_lambs:
        return len(current_fibo)
    else:
        return len(current_fibo) -1

def generous_solution(total_lambs):
    return int(log(total_lambs+1, 2))

def solution(total_lambs):
    #if (totaldd_lambs < 3):
    #    return 0
    return stingy_solution(total_lambs) - generous_solution(total_lambs)

