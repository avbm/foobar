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
            parent[state].append(element[-2])  # store parent with prior prob
        elif  visited_states[state] and loop(element, state, offset=-1):  # looped transition chain
            printd("loop {}".format(element))
            prior_prob = 1
            while element[0][0] != state:
                temp = element.pop(0)
                prior_prob *= temp[1]
            element[0] = (element[0][0], element[0][1]/prior_prob)
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

def get_transition_children(transition, children):
    parents = []
    printd("transition: {}".format(transition))
    for i in transition:
        parents.append(i[0])
    while len(parents) != 0:
        k = parents.pop()
        for i in parents:
            if i != k:
                #printd("i:{} k:{}".format(i, k))
                children[i][k] = True
    #printd("transition: {}\nchildren{}".format(transition, children))
    return children

def get_all_children(terminal_transitions, looped_transitions, n_states):
    children = []
    for i in range(n_states):
        children.append([])
        for j in range(n_states):
            children[i].append(False)
    for i in terminal_transitions.keys():
        parents = [i]
        for trans in terminal_transitions[i]:
            children = get_transition_children(trans, children)
    printd("transition children: {}".format(children))
    return children

def eval_terminal_probabilities(transitions, n_states):
    probs = [0] * n_states
    for i in range(n_states):
        if i in transitions.keys():
            aggj = Fraction(0)
            #printd(transitions[i])
            for j in range(len(transitions[i])):
                aggk = Fraction(1)
                for k in range(len(transitions[i][j])):
                    aggk *= transitions[i][j][k][1]
                #print(transitions[i][j])
                aggj += aggk
            probs[i] = aggj
    return probs

def eval_looped_probabilities(transitions, n_states, prior_probs, m, children):
    probs = [0] * n_states
    for i in range(n_states):
        if i in transitions.keys():
            aggj = Fraction(0)
            #printd(transitions[i])
            for j in range(len(transitions[i])):
                aggk = Fraction(1)
                for k in range(1, len(transitions[i][j])):
                    aggk *= transitions[i][j][k][1]
                #print(transitions[i][j])
                aggj += aggk
            
            # diving by prior prob to normalise
            if prior_probs[i] != 0:
                aggj = aggj/prior_probs[i]
            printd("i:{} agg:{}".format(i, aggj))

            probs[i] = 1 / (1 - aggj)  # infinite summation when agg<1
    printd("looped probabilities: {}".format(probs))
    for i in range(n_states):
        if probs[i] != 0:
            den = sum(m[i])
            for j in range(len(m[i])):
                if children[i][j]:
                    prior_probs[j] *= probs[i]
    return prior_probs

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
  
    parents = transitions[2]
    printd("parents: ".format(parents))
    children = get_all_children(transitions[0], transitions[1], len(m))
    probs = eval_looped_probabilities(transitions[1], 
            len(m), probs, m, children)
    printd("final_probs: {}".format(probs))

    # format output
    denominators = [sum(i) for i in m]
    stable_states = [i for i in range(len(denominators))
            if denominators[i] == 0]
    
    norm_factor = 1 / sum(probs)  # should ideally be 1
    probs = [ norm_factor * i for i in probs ]
    lcm = get_lcm(probs)

    ret_val = []
    den = 0
    for i in stable_states:
        ret_val.append(int(probs[i]*lcm))
    ret_val.append(lcm)
    return ret_val



