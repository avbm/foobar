try:
    from math import gcd
    from queue import Queue
except ImportError:
    from fractions import gcd
    from Queue import Queue
from collections import defaultdict
from fractions import Fraction
from copy import deepcopy


DEBUG = False
DEBUG = True

def printd(s):
    if DEBUG:
        print(s)

def is_loop(chain, state, offset=0):
    for element in chain[:len(chain)+offset]:
        if element[0] == state:
            return True
    return False

def get_state_transitions(m):
    terminal_transitions = defaultdict(lambda: list(), {})
    looped_transitions = defaultdict(lambda: list(), {})
    parents = defaultdict(lambda: list(), {})
    n_states = len(m)
    queue = Queue()
    visited_states = {}
    for i in range(len(m)):
        visited_states[i] = False

    queue.put([(0, Fraction(1))])  # put state id , prior probability
    while not queue.empty():
        element = queue.get()
        state = element[-1][0]
        prior_prob = element[-1][1]

        denominator = sum(m[state])
        if  visited_states[state] and is_loop(element, state, offset=-1):  # looped transition chain
            #printd("loop {}".format(element))
            prior_prob = 1
            while element[0][0] != state:
                temp = element.pop(0)
            #    prior_prob *= temp[1]
            #element[0] = (element[0][0], element[0][1]/prior_prob)
            looped_transitions[state].append(element)
        else:
            if not element in terminal_transitions[state]:
                terminal_transitions[state].append(element)
                if state != 0 and not element[-2][0] in parents[state]:
                    parents[state].append(element[-2][0])  # store parent

            visited_states[state] = True
            for i in range(len(m[state])):
                if m[state][i] != 0:
                    new_elem = deepcopy(element)
                    new_elem.append((i, Fraction(m[state][i], denominator)))
                    queue.put(new_elem)

    # We need to normalize the loops and remove duplicates
    # to do that we first pop last element to remove duplicate
    # then we rotate the loop so the min state value is the first node
    loops = []
    for i in looped_transitions.keys():
        chains = looped_transitions[i]
        #printd(transitions[i])
        for j in range(len(chains)):
            chain = chains[j]
            chain.pop(0)
            li = get_least_index(chain)
            while chain[0][0] != li:
                temp = chain.pop(0)
                chain.append(temp)
            if chain not in loops:
                loops.append(chain)
    printd("normalized loops: {}".format(loops))

    #recalculate transition fractions for loops
    for loop in loops:
        for i in range(len(loop)):
            s0 = loop[i][0]
            s1 = loop[(i+1)%len(loop)][0]
            fr = Fraction(m[s0][s1],sum(m[s0]))
            loop[i] = (s0, fr)

    printd("terminal_transitions: {}".format(terminal_transitions))
    printd("looped_transitions: {}".format(loops))
    return (terminal_transitions, loops, parents)


def eval_terminal_probabilities(transitions, n_states):
    probs = [0] * n_states

    for i in range(n_states):
        #aggj = Fraction(0)
        chains = transitions[i]
        #printd(transitions[i])
        for j in range(len(chains)):
            chain = chains[j]
            aggk = Fraction(1)
            for k in range(1, len(chain)):
                node = chain[k]
                aggk *= node[1]
            printd("state: {}, aggk: {}".format(i, aggk))
            probs[i] += aggk
    return probs

def get_least_index(chain):
    li = chain[0][0]
    for node in chain:
        li = min(li,node[0])
    return li

def eval_looped_probabilities(loops, parents,
        m, prior_probs):
    n_states = len(m)
    # loop_factor[i] = % or orig. value that comes back after one loop
    # for each state summed over all loops that state is a part of
    loop_factor = [0] * n_states
    for j in range(len(loops)):
        chain = loops[j]
        aggk = Fraction(1)
        for k in range(len(chain)):
            aggk *= chain[k][1]
        #print(transitions[i][j])
        aggk
        # aggk now represents the loop_factor for current loop
        # add aggk to each loop element's total
        # skip chain[0] since chain[0] = chain[-1]
        for k in range(len(chain)):
            loop_factor[chain[k][0]] += aggk
    printd("loop_factor: {}".format(loop_factor))

    agg_loop_factor = [0] * n_states

    for i in range(n_states):
        agg_loop_factor[i] = Fraction(1) / (1 - loop_factor[i])

    printd("agg_loop_factor: {}".format(agg_loop_factor))

    term_node_agg = [0] * n_states
    # now we need to calc sum of loop_factors*prior_probs*m[parent][term_node]
    # for terminal parent as a sum of the loop_factors of each parent
    for i in parents.keys():
        for ps in parents[i]:
            term_node_agg[i] += agg_loop_factor[ps] \
                                * prior_probs[ps] \
                                * Fraction(m[ps][i], sum(m[ps]))

    printd("term_node_agg: {}".format(term_node_agg))

    return term_node_agg

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
    transitions = get_state_transitions(m)
    prior_probs = eval_terminal_probabilities(transitions[0], len(m))
    printd("terminal_probs: {}".format(prior_probs))
    printd("parents: {}".format(transitions[2]))

    final_fractions = eval_looped_probabilities(transitions[1],
            transitions[2], m, prior_probs)
    printd("final_fractios: {}".format(final_fractions))

    # format output
    denominators = [sum(i) for i in m]
    stable_states = [i for i in range(len(denominators))
            if denominators[i] == 0]


    # Zero out non terminal remainders
    for i in range(len(m)):
        if not i in stable_states:
            final_fractions[i] = 0

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



