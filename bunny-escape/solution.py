try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from copy import deepcopy

DEBUG = True

def printd(s, debug=DEBUG):
    if debug:
        print(s)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, pos):
        return self.x == pos.x and self.y == pos.y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return "Position: " + self.__str__()

    def is_valid(self, map):
        if self.x < 0 or self.x >= len(map):
            return False
        elif self.y < 0 or self.y >= len(map[self.x]):
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
def get_path_length(map, marker=-1, INF=10000):
    queue = Queue()
    queue.put((Position(0,0), 1))
    while not queue.empty():
        element = queue.get()
        pos = element[0]
        printd("pos: {}".format(pos))
        path_length = element[1]
        
        if pos == Position(len(map)-1,len(map[-1])-1):
            return path_length
        else:
            if map[pos.x][pos.y] == marker:
                continue
            map[pos.x][pos.y] = marker
            nbrs = pos.get_neighbors(map)
            for n in nbrs:
                if map[n.x][n.y] != marker and not n.is_wall(map):
                    printd("adding nbr: {}".format(n))
                    queue.put((n, path_length + 1))
    return INF

def reset(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] < 0:  #!= 0 or map[i][j] !=1:
                map[i][j] = 0

def solution(map):
    marker = -1
    length = get_path_length(map, marker)
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 1:
                #temp_map = deepcopy(map)
                #temp_map[x][y] = 0
                #length = min(length, get_path_length(temp_map))

                if marker==-1: marker=-2
                else: marker=-1
                map[x][y]=0
                length = min(length, get_path_length(map, marker))
                map[x][y]=1

                #if length == len(map) + len(map[-1]) - 1:
                #    reset(map)
                #    return length
    reset(map)
    return length

def create_map(n):
    map = []
    for i in range(n):
        if i%2 == 0:
            map.append([0]*n)
        if i%4 == 3:
            map.append([1]*n)
            map[-1][0] = 0
        if i%4 == 1:
            map.append([1]*n)
            map[-1][-1] = 0
    return map

