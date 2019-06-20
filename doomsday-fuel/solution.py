try:
    from math import gcd
    from queue import Queue
except ImportError:
    from fractions import gcd
    from Queue import Queue
from collections import defaultdict
from fractions import Fraction as F
from copy import deepcopy


DEBUG = False
DEBUG = True

def printd(s, delay=0):
    if DEBUG:
        print(s)
        from time import sleep
        sleep(delay)

def is_loop(chain, state, offset=0):
    return state in chain[:len(chain)+offset]

def normalize_loops(loops, m):
    # here we will rotate loops so least state is the first element
    # then we will remove repeated loops
    n_states = len(m)
    norm_loops = []
    for loop in loops:
        min_state = min(loop)
        while loop[0] != min_state:
            state = loop.pop(0)
            loop.append(state)
        if not loop in norm_loops:
            norm_loops.append(loop)
    return norm_loops

def traverse_m(m):  # assumes m has been converted to fractions
    paths = []
    path = [0]
    loops = []
    n_states = len(m)
    visited_states = [False]*n_states
    parents = defaultdict(lambda: list(), {})
    queue = Queue()
    queue.put(path)  # we always start with state 0
    path_tree = defaultdict(lambda: list(), {})  # parent: list of children
    lin_vals = [0]*n_states
    while not queue.empty():
        path = queue.get()
        state = path[-1]
        if visited_states[state] and is_loop(path, state, -1):
            # This is a loop
            path.pop()
            while path[0] != state:
                path.pop(0)
            loops.append(path)
        else:
            # not a loop get children and continue
            visited_states[state] = True
            if sum(m[state]) == 0:
                # terminal state
                paths.append(path)
                parents[state].append(path[-2])
            else:
                #printd("c3: path: {}".format(path))
                if state == 0:
                    lin_vals[0] = 1
                else:
                    lin_vals[state] += lin_vals[path[-2]]*m[path[-2]][state]
                for i in range(n_states):
                    if m[state][i] != 0:
                        path_tree[state].append(i)
                        new_path = deepcopy(path)
                        new_path.append(i)
                        queue.put(new_path)
    printd("paths: {}".format(paths))
    path_tree = dict(path_tree)
    printd("path_tree: {}".format(path_tree))

    printd("loops: {}".format(loops))
    parents = dict(parents)
    printd("parents: {}".format(parents))

    norm_loops = normalize_loops(loops, m) 
    printd("norm_loops: {}".format(norm_loops))


    return (paths, norm_loops, parents, lin_vals)

def calc_linear_values(path_tree, m):
    n_states = len(m)
    lin_vals = [0]*n_states
    lin_vals[0] = 1
    for i in range(len(m)):
        agg = 1
        for i in range(1, len(path)):
            ps = path[i-1]
            cs = path[i]
            agg *= m[ps][cs]
            lin_vals[cs] += agg
    return lin_vals

def calc_loop_gains(loops, m):
    loop_iter = [0]*len(m)
    printd("input loops: {}".format(loops))
    printd("input m: {}".format(m))
    for loop in loops:
        agg = 1
        len_loop = len(loop)
        for i in range(len_loop):
            cs = loop[i]               # current state
            ns = loop[(i+1)%len_loop]  # parent state
            #printd("cs:{} ns:{} m[cs][ns]:{}".format(cs, ns, m[cs][ns]))
            agg *= m[cs][ns]
 
        for state in loop:
            loop_iter[state] += agg

    printd("loop_iter: {}".format(loop_iter))

    loop_gains = [F(1)/(1-i) for i in loop_iter]
    printd("loop_gains: {}".format(loop_gains))
    return loop_gains

def calc_final_states(parents, m, linear_vals, loop_gains):
    final_states = [0] * len(m)
    for term_state in parents.keys():
        for parent in parents[term_state]:
            printd("linear_val:{} loop_gain:{} m_val: {}".format(linear_vals[parent], loop_gains[parent], m[parent][term_state]))
            prod = linear_vals[parent] \
                    * loop_gains[parent] \
                    * m[parent][term_state]
            printd("parent:{} term_state:{} prod:{}".format(parent, 
                term_state, prod))
            final_states[term_state] += prod
    return final_states

def lcm(a, b):
    if a==0 and b==0:
        return 0
    else:
        return a*b // gcd(a,b)

def get_lcm(fracs):
    base = fracs[0].denominator
    for i in range(len(fracs)):
        base = lcm(base, fracs[i].denominator)
    return base

def solution(m):
    mf = deepcopy(m)
    for row in mf:
        sum_r = sum(row)
        if sum_r != 0:
            for i in range(len(row)):
                row[i] = F(row[i], sum_r)  # convert m to fractions

    (paths, loops, parents, linear_vals) = traverse_m(mf)

    #linear_vals = calc_linear_values(paths, mf)
    printd("linear_vals: {}".format(linear_vals))
    loop_gains = calc_loop_gains(loops, mf)
    final_states = calc_final_states(parents, mf, linear_vals, loop_gains)
    # format output
    denominators = [sum(i) for i in m]
    stable_states = [i for i in range(len(denominators))
            if denominators[i] == 0]

    final_fractions = final_states
    # normalize final_fractions
    total = sum(final_fractions)
    final_fractions = [i/total for i in final_fractions]

    lcm = get_lcm(final_fractions)

    printd("final_fractions: {}".format(final_fractions))
    printd("lcm: {}".format(lcm))
    ret_val = []
    den = 0
    for i in stable_states:
        #printd("i:{} f_i:{}".format(i, final_fractions[i]))
        ret_val.append(int(final_fractions[i]*lcm))
    ret_val.append(lcm)
    return ret_val

