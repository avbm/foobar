try:
    from math import gcd
except ImportError:
    from fractions import gcd

DEBUG = True
THRESHOLD = 2**16

def printd(s, sleep_time=0):
    if DEBUG:
        print(s)
        from time import sleep
        sleep(sleep_time)

def changed(state, next_state):
    ret_val = False
    for i in range(len(state)):
        if state[i] != next_state[i]:
            ret_val = True
    return ret_val

def lcm(a, b):
    if a==0 and b == 0:
        return 0
    else:
        return a*b // gcd(a,b)

def gcd_state(state):
    base = state[0]
    for i in state:
        base = gcd(base, i)
        #print("i:{} gcd:{}".format(i, base))
    #printd("gcd: {}".format(base))
    return base

def lcm_state(state):
    base = 1
    for i in state:
        if i != 0:
            base = lcm(base, i)
    return base

def normalize_state(state):
    gcd = gcd_state(state)
    state = [ i//gcd for i in state ]
    return state

def update_state(m, curr_state, stable_states):

    n_states = len(m)
    next_state = [0]* n_states
    denominators = [sum(i) for i in m]
    base = lcm_state(denominators)
    weights = []
    for i in range(len(denominators)):
        if denominators[i] == 0:
            weights.append(base)
        else:
            weights.append(base // denominators[i])

    for i in range(n_states):
        if i in stable_states:
            next_state[i] += weights[i] * curr_state[i]
        else:
            for j in range(n_states):
                next_state[j] += weights[i] * curr_state[i] * m[i][j]
    next_state = normalize_state(next_state)
    return next_state

def run_transitions(m):
    n_states = len(m)
    state = [0] * n_states
    state[0] = 1
   
    denominators = [sum(i) for i in m]
    stable_states = [i for i in range(len(denominators))
            if denominators[i] == 0]
    printd("stable_states: {}".format(stable_states))

    state_changed = True

    next_state = update_state(m, state, stable_states)
    while state_changed:
        next_state = update_state(m, state, stable_states)
        state_changed = changed(state, next_state)
        printd("old state: {}".format(state))
        printd("new state: {}".format(next_state), 1)
        state = next_state
    return next_state

def solution(m):
    denominators = [sum(i) for i in m]
    stable_states = [i for i in range(len(denominators))
            if denominators[i] == 0]

    final_state = run_transitions(m)
    ret_val = []
    den = 0
    for i in stable_states:
        ret_val.append(final_state[i])
        den += final_state[i]
    ret_val.append(den)
    return ret_val
    
