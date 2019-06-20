try:
    from math import gcd
except ImportError:
    from fractions import gcd

THRESHOLD = 100  # 1/THRESHOLD is the smallest possible change
DEBUG = True

def printd(s, sleep_time=0):
    if DEBUG:
        print(s)
        from time import sleep
        sleep(sleep_time)

class Probability:
    def __init__(self):
        self.num = 0
        self.den = 1

    def __init__(self, num, den):
        #num/den
        self.num = num
        self.den = den
        self.sanitize()

    def __eq__(self, p):
        self.sanitize()
        p.sanitize()
        return self.num == p.num and self.den == p.den

    def __str__(self):
        return "P({}/{})".format(self.num, self.den)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, p):
        return self.num * p.den > p.num * self.den

    def __lt__(self, p):
        return self.num * p.den < p.num * self.den

    def add(self, p):
        ret = Probability(self.num*p.den + self.den*p.num, self.den*p.den)
        ret.sanitize()
        return ret

    def mult(self, p):
        ret = Probability(self.num*p.num, self.den*p.den)
        ret.sanitize()
        return ret

    def sanitize(self):
        if self.num == 0:
            #printd("sanitize called: {}".format(self))
            self.den = 1
        elif self.den == 0:
            printd("ERROR: denominator is 0 {}".format(self))
            self.num/self.den  # should throw exception
        else:
            div = gcd(self.num, self.den)
            self.num = self.num / div
            self.den = self.den / div
        return self

    def eval(self)mport:
        self.sanitize()
        return (1.00*self.num) / self.den

def redistribute_small_remainder(state, m):
    min_index = 0
    max_index = 0
    for i in range(len(state)):
        if state[i].num !=0 and state[min_index] > state[i]:
            min_index = i
        if state[max_index] < state[i]:
            max_index = i
    if state[min_index].den >= THRESHOLD:
        for i in range(len(m)):
            m[i][min_index] = 0
    return state

def update_state(m, curr_state):

    denominators = [sum(i) for i in m]
    #printd("denominators: {}".format(denominators))
    next_state = [Probability(0,1)]*len(m)
    #printd("initial cumu state: {}:".format(next_state), sleep_time=1) 

    # state transitions
    for i in range(len(m)):
        # add initial ore quantities for stable states
        if denominators[i] == 0:
            next_state[i] = next_state[i].add(curr_state[i])
            #printd("static cumu state: {}:".format(next_state))
        else:
            for j in range(len(m[i])):
                #printd("curr_state[i]: {}".format(curr_state[i]))
                #printd("m[i][j]: {}".format(m[i][j]))
                next_state[j] = next_state[j].add(
                        Probability(curr_state[i].num * m[i][j],
                            curr_state[i].den * denominators[i]))
                #printd("next_state updated: {} {}".format(j, next_state[j]))
        #printd("next_state: {}".format(next_state), 1)
    #printd("final next_state: {}:".format(next_state), 1) 
    
    temp = Probability(0,1)
    for p in next_state:
        temp = temp.add(p)
    if temp.num != temp.den:
        1/0
    return next_state

def changed(state, new_state):
    state_changed = False
    for i in range(len(state)):
        num = abs(new_state[i].num * state[i].den
                - new_state[i].den * state[i].num)
        den = new_state[i].den * state[i].den
        if num != 0 and den/num < THRESHOLD:
            state_changed = True
    return state_changed

def changed2(state, new_state):
    state_changed = False
    for i in range(len(state)):
        if not state[i] == new_state[i]:
            state_changed = True
    return state_changed

def run_transitions(m):
    # initial state, all ore in state 0
    state = [Probability(0,1)]*len(m)
    state[0] = Probability(1,1)

    printd("Initial state: {}".format(state), 1)
    state_changed = True
    while state_changed:
        printd("old state: {}".format(state))
        new_state = update_state(m, state)
        new_state = redistribute_small_remainder(new_state, m)

        printd("new state: {}".format(new_state), 1)

        state_changed = changed2(state, new_state)
        state = new_state
    return state

def lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return (a*b) // gcd(a, b)

def solution(m):
    final_state = run_transitions(m)
    ans = []
    denominator = 1
    for prob in final_state:
        denominator = lcm(denominator, prob.den)

    denominators = [sum(i) for i in m]
    for i in range(len(final_state)):
        if denominators[i] == 0:
            if final_state[i].num == 0:
                ans.append(0)
            else:
                val = final_state[i].num * (denominator/final_state[i].den)
                ans.append(val)
    ans.append(denominator)
    return ans


