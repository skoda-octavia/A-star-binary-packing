import queue

cases = [
    (2,12),
    (7,12),
    (8,6),
    (3,6),
    (3,5),
    (5,5),
    (3,12),
    (3,7),
    (5,7),
    (2,6),
    (3,2),
    (4,2),
    (3,4),
    (4,4),
    (9,2),
    (11,2)
]

class Node:
    def __init__(self, bin_config: list[bool]) -> None:
        self.bin_config = bin_config

    def valid_config() -> bool:
        pass

    def heuristic(self, container_size: float) -> float:
        priority_queue = queue.PriorityQueue()
        for width, height in cases:
            priority_queue.put(width * height)
        temp_size = 0
        size = 0
        val = 0
        while True:
            temp_size = priority_queue.get()
            if size + temp_size >= container_size:
                val += (container_size - size) / temp_size
                return val
            else:
                size += temp_size
                val += 1 

    def children(self) -> list:
        node_false = Node(self.bin_config + [False])
        node_true = Node(self.bin_config + [True])
        return [node_false, node_true]

    def final(self) -> bool:
        return len(self.bin_config) == len(cases)


def a_star():
# 1.  Initialize the open list
    opendList = []

# 2.  Initialize the closed list
#     put the starting node on the open 
#     list (you can leave its f at zero)
    priority_queue = queue.PriorityQueue()
    prime_node = Node([])
    priority_queue.put(0, prime_node)
# 3.  while the open list is not empty
#     a) find the node with the least f on 
#        the open list, call it "q"
    # while len(nodes) != 0:


#     b) pop q off the open list
  
#     c) generate q's 8 successors and set their 
#        parents to q
   
#     d) for each successor
#         i) if successor is the goal, stop search
        
#         ii) else, compute both g and h for successor
#           successor.g = q.g + distance between 
#                               successor and q
#           successor.h = distance from goal to 
#           successor (This can be done using many 
#           ways, we will discuss three heuristics- 
#           Manhattan, Diagonal and Euclidean 
#           Heuristics)
          
#           successor.f = successor.g + successor.h

#         iii) if a node with the same position as 
#             successor is in the OPEN list which has a 
#            lower f than successor, skip this successor

#         iV) if a node with the same position as 
#             successor  is in the CLOSED list which has
#             a lower f than successor, skip this successor
#             otherwise, add  the node to the open list
#      end (for loop)
  
#     e) push q on the closed list
#     end (while loop)