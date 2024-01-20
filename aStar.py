import queue
from Packer import pack_rects
from Plot import initialize_plot, update_gloabl_plot, freeze
from Rectangle import Rectangle as Rect
from Configuration import Configuration

MAX_INT = 2**31 - 1

class DeterministicPriorityQueue(queue.PriorityQueue):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def put(self, item):
        super().put((item[0], self.counter, item[1]))
        self.counter += 1 

class Node:
    all_rects: list[tuple[float, float]] = []
    con_sizes: tuple[float, float]
    con_area: float

    def __init__(self, bin_config: list[bool], parent_config: Configuration=None):
        self.bin_config = bin_config
        self.con_area = Node.con_sizes[0] * Node.con_sizes[1]
        self.valid = self.get_valid_config(parent_config)
        self.heuristic = self.get_heuristic()
        self.final = self.get_final()
        self.profit = self.get_profit()
        self.value = self.get_value()


    def get_valid_config(self, parent_config: Configuration=None) -> bool:
        if parent_config is not None:
            self.config = parent_config
            return True
        temp_size = 0
        used_rects = []
        for element, decision in zip(Node.all_rects, self.bin_config):
            if decision:
                used_rects.append(element)
                w, h = element
                temp_size += w * h
                if temp_size > Node.con_area:
                    return False
        config = pack_rects(used_rects, Node.con_sizes)
        if config is None:
            return False
        else:
            self.config = config
        return True

    def get_heuristic(self) -> float:
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
                return val
            else:
                size += temp_size
                val += 1 
        return val

    def children(self) -> list:
        node_false = Node(self.bin_config + [False], self.config)
        node_true = Node(self.bin_config + [True])
        return [node_false, node_true]

    def get_final(self) -> bool:
        return len(self.bin_config) == len(Node.all_rects)
    
    def get_profit(self) -> int:
        if not self.valid:
            return  -MAX_INT
        return sum(self.bin_config)
    
    def get_value(self) -> float:
        return self.profit + self.heuristic


def a_star(prime_node: Node):
    max_profit = 0
    max_possible_profit = len(Node.all_rects)
    best_configuration = None
    priority_queue = DeterministicPriorityQueue()
    priority_queue.put((-prime_node.value, prime_node))
    while not priority_queue.empty():
        node = priority_queue.get()[2]
        if node.final:
            profit = node.profit
            if profit > max_profit:
                max_profit = profit
                best_configuration = node.config
                if Configuration.plotting:
                    update_gloabl_plot(best_configuration)
                if profit == max_possible_profit:
                    return best_configuration
        else:
            for child in node.children():
                if child.valid and child.value > max_profit:
                    priority_queue.put((-child.value, child))
    return best_configuration

cases = [
    (4,1),
    (4,5),
    (9,4),
    (3,5),
    (3,9),
    (1,4),
    (5,3),
    (4,1),
    (5,5),
    (7,2),
    (9,3),
        (6,2),
    (4,6),
    (6,3),
    (10,3),
    (6,3),
    (6,3),
    (10,3)
]

def run(
        cases: list[tuple[float, float]],
        container_size: tuple[float, float]=(15, 15),
        plotting: bool=True
        ):
    if plotting:
        cases_rects = [Rect((0, 0), x[0], x[1], False) for x in cases]
        config = Configuration(container_size, cases_rects, plot=False)
        initialize_plot(config, cases_rects, container_size)
        update_gloabl_plot(config)
    Configuration.plotting = plotting
    Node.all_rects = cases
    Node.con_sizes = container_size
    Node.con_area = container_size[0] * container_size[1]
    prime_node = Node([])
    best_config = a_star(prime_node)
    if plotting:
        freeze()


if __name__ == "__main__":
    run(cases)
