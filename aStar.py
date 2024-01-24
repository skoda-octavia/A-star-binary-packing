import queue
from Plot import initialize_plot, update_gloabl_plot, freeze
from Rectangle import Rectangle as Rect
from Configuration import Configuration
from Node import Node
from time import time

class DeterministicPriorityQueue(queue.PriorityQueue):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def put(self, item):
        super().put((item[0], self.counter, item[1]))
        self.counter += 1 

def a_star(prime_node: Node):
    max_profit = 0
    max_possible_profit = len(Node.all_rects)
    best_configuration = None
    priority_queue = DeterministicPriorityQueue()
    priority_queue.put((-prime_node.value, prime_node))
    while not priority_queue.empty():
        node = priority_queue.get()[2]
        profit = node.profit
        if profit > max_profit and node.valid:
            max_profit = profit
            best_configuration = node.config
            print(f"Found configuration {profit}/{max_possible_profit}")
            if Configuration.plotting:
                update_gloabl_plot(best_configuration)
            if profit == max_possible_profit:
                return best_configuration
        if not node.final:
            for child in node.children():
                if child.valid and child.value > max_profit:
                    priority_queue.put((-child.value, child))
    return best_configuration


def a_star_time_capture(prime_node: Node):
    times = {}
    max_profit = 0
    max_possible_profit = len(Node.all_rects)
    best_configuration = None
    priority_queue = DeterministicPriorityQueue()
    priority_queue.put((-prime_node.value, prime_node))
    start_time = time()
    while not priority_queue.empty():
        node = priority_queue.get()[2]
        profit = node.profit
        if profit > max_profit:
            end_time = time()
            max_profit = profit
            best_configuration = node.config
            times[max_profit] = end_time - start_time
            print(f"Found configuration {profit}/{max_possible_profit}")
            if Configuration.plotting:
                update_gloabl_plot(best_configuration)
            if profit == max_possible_profit:
                return best_configuration
        if not node.final:
            for child in node.children():
                if child.valid and child.value > max_profit:
                    priority_queue.put((-child.value, child))
    return best_configuration, times


def run(
        func: callable,
        cases: list[tuple[float, float]],
        container_size: tuple[float, float]=(15, 15),
        plotting: bool=True,
        final_plot: bool=True
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
    resoult = func(prime_node)
    if plotting:
        freeze()
    elif final_plot:
        cases_rects = [Rect((0, 0), x[0], x[1], False) for x in cases]
        initialize_plot(resoult, cases_rects, container_size)
        update_gloabl_plot(resoult)
        freeze()
    return resoult
