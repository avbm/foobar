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

def loop(chain, state, offset=0):
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
        if denominator == 0:  # reached a terminal state
            terminal_transitions[state].append(element)
            parents[state].append(element[-2])  # store parent with prior prob
        elif  visited_states[state] and loop(element, state, offset=-1):  # looped transition chain
            #printd("loop {}".format(element))
            prior_prob = 1
            while element[0][0] != state:
                temp = element.pop(0)
            #    prior_prob *= temp[1]
            #element[0] = (element[0][0], element[0][1]/prior_prob)
            looped_transitions[state].append(element)
        else:
            visited_states[state] = True
            for i in range(len(m[state])):
                if m[state][i] != 0:
                    new_elem = deepcopy(element)
                    new_elem.append((i, Fraction(m[state][i], denominator)))
                    queue.put(new_elem)

    printd("terminal_transitions: {}".format(terminal_transitions))
    printd("looped_transitions: {}".format(looped_transitions))
    return (terminal_transitions, looped_transitions, parents)


def eval_terminal_probabilities(transitions, n_states, node_weights=None):
    probs = [0] * n_states
    if node_weights is None:
        node_weights = [1] * n_states

    for i in range(n_states):
        if i in transitions.keys():
            aggj = Fraction(0)
            chains = transitions[i]
            #printd(transitions[i])
            for j in range(len(chains)):
                chain = chains[j]
                aggk = Fraction(1)
                for k in range(len(chain)):
                    node = chain[k]
                    aggk *= node[1]*node_weights[node[0]]
                #print(transitions[i][j])
                aggj += aggk
            probs[i] = aggj
    return probs

def eval_looped_probabilities(transitions, terminal_transitions,
        n_states, prior_probs):
    probs = [0] * n_states
    for i in transitions.keys():
        chains = transitions[i]
        aggj = Fraction(0)
        #printd(transitions[i])
        for j in range(len(chains)):
            chain = chains[j]
            aggk = Fraction(1)
            for k in range(1, len(chain)):
                aggk *= chain[k][1]
            #print(transitions[i][j])
            aggj += aggk
        
        # diving by prior prob to normalise
        if prior_probs[i] != 0:
            aggj = aggj/prior_probs[i]
        printd("i:{} agg:{}".format(i, aggj))

        probs[i] = 1 / (1 - aggj)  # infinite summation when agg<1
    printd("looped probabilities: {}".format(probs))

    loop_node_weights = probs
    #for i in range(n_states):
    #    if probs[i] == 0:
    #        probs[i] = 1
    #weighted_probs = eval_terminal_probabilities(terminal_transitions, n_states, probs)
    final_probs = [0] * n_states
    for i in terminal_transitions.keys():
        for chain in terminal_transitions[i]:
            loop_node_wt = 1
            agg = 1
            for node in chain:
                if node[0] in transitions.keys() and loop_node_wt == 1:
                    loop_node_wt = loop_node_weights[node[0]]
                agg *= node[1]
            final_probs[i] += agg * loop_node_wt
    return final_probs

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
    probs = eval_terminal_probabilities(transitions[0], len(m))
    printd("terminal_probs: {}".format(probs))
  
    #parents = transitions[2]
    #printd("parents: {}".format(parents))

    probs = eval_looped_probabilities(transitions[1], transitions[0], 
            len(m), probs)
    printd("final_probs: {}".format(probs))

    # format output
    denominators = [sum(i) for i in m]
    stable_states = [i for i in range(len(denominators))
            if denominators[i] == 0]
    
    #norm_factor = 1 / sum(probs)  # should ideally be 1
    #probs = [ norm_factor * i for i in probs ]
    lcm = get_lcm(probs)

    ret_val = []
    den = 0
    for i in stable_states:
        ret_val.append(int(probs[i]*lcm))
    ret_val.append(lcm)
    return ret_val



