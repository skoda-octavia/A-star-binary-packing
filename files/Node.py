from Configuration import Configuration
from Packer import pack_rects
import queue

MAX_INT = 2**31 - 1

class Node:
    all_rects: list[tuple[float, float]] = []
    con_sizes: tuple[float, float]
    con_area: float

    def __init__(self, bin_config: list[bool], parent_config: Configuration=None):
        self.bin_config = bin_config
        self.set_valid_config(parent_config)
        self.set_heuristic()
        self.set_final()
        self.set_profit()
        self.set_value()


    def set_valid_config(self, parent_config: Configuration=None) -> None:
        if parent_config is not None:
            self.config = parent_config
            self.valid = True
            return
        temp_size = 0
        used_rects = []
        for element, decision in zip(Node.all_rects, self.bin_config):
            if decision:
                used_rects.append(element)
                w, h = element
                temp_size += w * h
                if temp_size > Node.con_area:
                    self.valid = False
                    self.config = None
                    return
        config = pack_rects(used_rects, Node.con_sizes)
        if config is None:
            self.valid = False
            self.config = None
            return
        else:
            self.config = config
        self.valid = True


    def set_heuristic(self) -> None:
        priority_queue = queue.PriorityQueue()
        not_used_cases = Node.all_rects[len(self.bin_config):]
        for width, height in not_used_cases:
            priority_queue.put(width * height)
        temp_size = 0
        size = 0
        val = 0
        while not priority_queue.empty():
            temp_size = priority_queue.get()
            if size + temp_size >= Node.con_area:
                val += (Node.con_area - size) / temp_size
                self.heuristic = val
                return
            else:
                size += temp_size
                val += 1 
        self.heuristic = val

    def children(self) -> list:
        node_false = Node(self.bin_config + [False], self.config)
        node_true = Node(self.bin_config + [True])
        return [node_false, node_true]

    def set_final(self) -> None:
        self.final = len(self.bin_config) == len(Node.all_rects)
    
    def set_profit(self) -> int:
        if not self.valid:
            self.profit = -MAX_INT
            return
        self.profit = sum(self.bin_config)
    
    def set_value(self) -> float:
        self.value = self.profit + self.heuristic