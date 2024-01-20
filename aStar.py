import queue
from Packer import pack_rects
from Plot import initialize_plot, PLOT

MAX_INT = 2**31 - 1

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
    def __init__(self, bin_config: list[bool], con_sizes: tuple[float, float]):
        self.bin_config = bin_config
        self.con_sizes = con_sizes
        self.con_size = con_sizes[0] * con_sizes[1]

    def valid_config(self) -> bool:
        temp_size = 0
        used_rects = []
        for element, decision in zip(cases, self.bin_config):
            if decision:
                used_rects.append(element)
                w, h = element
                temp_size += w * h
                if temp_size > self.con_size:
                    return False
        config = pack_rects(used_rects, self.con_sizes)
        if config is None:
            return False
        else:
            self.config = config
        return True

    def heuristic(self) -> float:
        priority_queue = queue.PriorityQueue()
        not_used_cases = cases[len(self.bin_config):]
        for width, height in not_used_cases:
            priority_queue.put(width * height)
        temp_size = 0
        size = 0
        val = 0
        while True:
            temp_size = priority_queue.get()
            if size + temp_size >= self.con_size:
                val += (self.con_size - size) / temp_size
                return val
            else:
                size += temp_size
                val += 1 

    def children(self) -> list:
        node_false = Node(self.bin_config + [False], self.con_sizes)
        node_true = Node(self.bin_config + [True], self.con_sizes)
        return [node_false, node_true]

    def final(self) -> bool:
        return len(self.bin_config) == len(cases)
    
    def profit(self) -> int:
        if not self.valid_config():
            return  -MAX_INT
        return sum(self.bin_config)
    
    def value(self) -> float:
        return self.profit() + self.heuristic()


def a_star():
    max_profit = 0
    best_configuration = None
    priority_queue = queue.PriorityQueue()
    prime_node = Node([], (18, 18))
    priority_queue.put((-prime_node.value(), prime_node))
    # if PLOT:
    #     initialize_plot(, config_rects)
    while not priority_queue.empty():
        node = priority_queue.get()[1]
        for child in node.children():
            if child.final():
                profit = child.profit()
                if profit > max_profit:
                    max_profit = profit
                    best_configuration = child.config
                else:
                    value = child.profit() + child.heuristic()
                    if value > max_profit:
                        priority_queue.put((-value, child))
            else:
                value = child.value()
                if value > 0:
                    priority_queue.put((-value, child))
    return best_configuration



if __name__ == "__main__":
    a_star()
