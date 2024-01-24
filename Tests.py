import random
from aStar import run, a_star, a_star_time_capture

ELEMENTS_RATIO = 1.3
ELEMENTS_NUMBER = 16
MAX_EL_LEN_RATIO = 0.7
MIN_EL_LEN_RATIO = 0.3

def set_seed(rand_seed: int):
    random.seed(rand_seed)

def get_seed(file_name: str="seed.txt") -> int:
    rand_seed = 42
    try:
        with open(file_name, "r") as file:
            line = file.readline()
            rand_seed = int(line)
    except Exception:
        print(f"Could not read random seed from file: {file_name}")
    return rand_seed

def reduce_sizes(target, elements):
    min_el_size = 2
    while target < sum([el[0] * el[1] for el in elements]):
        random_index = random.randint(0, len(elements) - 1)
        temp_elements = elements[random_index]
        if max(temp_elements) > min_el_size and min(temp_elements) > min_el_size:
            reduced = random.choice([(min(temp_elements), max(temp_elements) -1), (min(temp_elements) -1, max(temp_elements))])
            elements[random_index] = reduced

def generate_float_tuples(num_tuples, con_len, max_elem_ratio, min_elem_ratio):
    tuples = []
    edges = (con_len*min_elem_ratio, con_len*max_elem_ratio)
    for i in range(num_tuples):
        float1 = random.uniform(edges[0], edges[1])
        float2 = random.uniform(edges[0], edges[1])
        tuples.append((float1, float2))
    return tuples

def generate_int_tuples(num_tuples, con_len, max_elem_ratio, min_elem_ratio):
    tuples = []
    edges = (int(con_len*min_elem_ratio), int(con_len*max_elem_ratio))
    for _ in range(num_tuples):
        int1 = random.randint(edges[0], edges[1])
        int2 = random.randint(edges[0], edges[1])
        tuples.append((int1, int2))
    return tuples

def float_int_comparation_test():
    cases: list[tuple[float, float]]
    container_size: tuple[float, float]=(15, 15)
    plotting: bool=True
    float_elem = generate_float_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
    int_elem = generate_int_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
    reduce_sizes(container_size[0] * container_size[1], float_elem)
    reduce_sizes(container_size[0] * container_size[1], int_elem)
    float_size = 0
    for tup in float_elem:
        float_size += tup[0] * tup[1]
        print(tup)
    print(float_size)

    el_sizes = 0
    for ints in int_elem:
        print(ints)
        el_sizes += ints[0] * ints[1]
    print(el_sizes)


def float_int_quality_test():
    tests_num = 10
    int_sum = 0
    float_sum = 0
    container_size: tuple[float, float]=(15, 15)
    for i in range(tests_num):
        set_seed(get_seed() + i)
        float_elem = generate_float_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
        int_elem = generate_int_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
        reduce_sizes(container_size[0] * container_size[1] *ELEMENTS_RATIO, float_elem)
        reduce_sizes(container_size[0] * container_size[1]*ELEMENTS_RATIO, int_elem)
        config = run(a_star, float_elem, container_size, False, False)
        if config is not None:
            float_sum += len(config.packed_rects)
        config = run(a_star, int_elem, container_size, False, False)
        if config is not None:
            int_sum += len(config.packed_rects)
    print(f"Mean for ints: {int_sum/tests_num}")
    print(f"Mean for floats: {float_sum/tests_num}")



if __name__ == "__main__":
    float_int_quality_test()