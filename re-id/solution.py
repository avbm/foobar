from math import sqrt

CURRENT_PRIMES = ['2']

def is_prime(number, current_primes = ['2']):
    if str(number) in current_primes:
        return True
    else:
        for i in current_primes:
            if number % int(i) == 0: # i is string so type conversion
                return False
        for i in range(int(current_primes[-1]) + 1, int(sqrt(number))+1):
            if number % i == 0:  # i is an int here already
                return False
        return True

def get_next_prime(current_primes):
    if len(current_primes) == 0:
        current_primes.append('2')
        return 2
    else:
        i = int(current_primes[-1]) + 1
        while True:
            if is_prime(i, current_primes):
                current_primes.append(str(i))
                return i
            i += 1

def grow_prime_string(desired_len, prime_string, current_primes):
    while len(prime_string) < desired_len:
        next_prime = get_next_prime(current_primes)
        #current_primes.append(str(next_prime))
        prime_string += str(next_prime)
    return prime_string
    
def get_id(i, current_primes, id_len=5):
    prime_string = "".join(current_primes)
    if i+id_len > len(prime_string):
        prime_string = grow_prime_string(i+id_len, prime_string, current_primes)
    return prime_string[i: i+id_len]  # get_id(i, current_primes)

def solution(i):
    # Your code here
    return get_id(i, CURRENT_PRIMES)

