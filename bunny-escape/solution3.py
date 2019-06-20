try:
    from queue import Queue
except ImportError:
    from Queue import Queue

from copy import deepcopy


def printd(s, debug=False):
    if debug:
        print(s)

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, pos):
        return self.x == pos.x and self.y == pos.y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return self.__str__()

    def is_valid(self, map):
        if self.x < 0 or self.x >= len(map):
            return False
        elif self.y < 0 or self.y >= len(map[0]):
            return False
        return True

    def get_neighbors(self, map):
        nbrs = []
        for step in ((1,0),(0,1),(-1,0),(0,-1)):
            pos = Position(self.x + step[0], self.y + step[1])
            if pos.is_valid(map):
                nbrs.append(pos)
        return nbrs

    def is_wall(self, map):
        if map[self.x][self.y] == 1:
            return True
        else:
            return False

    def is_passable(self, map):
        if map[self.x][self.y] == 0:
            return True
        else:
            return False
            
# INF represents number longer than longest possible path
def get_path_length(map, INF=1000):
    queue = Queue()
    queue.put((Position(0,0), 1))
    while not queue.empty():
        element = queue.get()
        pos = element[0]
        printd("pos: {}".format(pos))
        path_length = element[1]
        if pos == Position(len(map)-1,len(map[0])-1):
            return path_length
        else:
            map[pos.x][pos.y] = 1
            nbrs = pos.get_neighbors(map)
            for n in nbrs:
                if n.is_passable(map):
                    printd("adding nbr: {}".format(n))
                    map[pos.x][pos.y] = -1  # marker var to track covered positions
                    queue.put((n, path_length + 1))
    return INF

def reset(map):
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == -1:
                map[x][y] = 0

def solution(map):
    length = get_path_length(map)
    reset(map)
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == 1:
                #temp_map = deepcopy(map)
                map[x][y] = 0
                length = min(length, get_path_length(map))
                reset(map)
    return length
