from Configuration import Configuration
from Rectangle import Rectangle as Rect
from copy import deepcopy, copy
import matplotlib.pyplot as plt 
from Plot import initialize_plot, update_temp_plot, clear_plot

class Packer:

    def __init__(self, configuration: Configuration) -> None:
        if configuration is None:
            raise ValueError("Configuration in null")
        else:
            self.config = configuration

    def A0(self, C: Configuration) -> Configuration:
        while C.L:

            degrees = [self.degree(rect, C) for rect in C.L]
            bestIdx = degrees.index(max(degrees))
            C.place_rect(C.L[bestIdx])
        return C

    def benefit_A1(self, rect: Rect, C_copy: Configuration):
        C_copy.place_rect(rect)
        C_copy = self.A0(C_copy)

        if C_copy.successful():
            return C_copy
        else:
            return C_copy.density()


    def degree(self, rect: Rect, config: Configuration) -> float:
        min_distances = []
        for packed_rect in config.packed_rects:
            min_distances.append(rect.min_distance_from(packed_rect))
        # distances from edges
        min_distances += [rect.placed_x, rect.placed_y]
        min_distances += [config.width - rect.top_x, config.height - rect.top_y]

        # min distance only for connected rects not by default (always two)
        min_distances.remove(min(min_distances))
        min_distances.remove(min(min_distances))

        return 1 - (min(min_distances)/((rect.width + rect.height)/2))
    
    def A1(self, config: Configuration):
        while config.L:
            max_benefit = 0
            best_ccoa = None
            for ccoa in config.L:
                d = self.benefit_A1(ccoa, deepcopy(config))
                if isinstance(d, Configuration):
                    print("fount one")
                    return d
                else:
                    if max_benefit < d:
                        max_benefit = d
                        best_ccoa = ccoa
            print(f"Placed {max_benefit}, {len(config.not_packed_rects)} rects remaining")
            config.place_rect(best_ccoa)

        if config.successful():
            print("Found successful configuration")
            return config
        else:
            print("Stopped with failure")
            return None


def pack_rects(rects: list[tuple], con_size: tuple[float, float]) -> Configuration:
    config_rects = [Rect((0, 0), x[0], x[1], False) for x in rects]
    C = Configuration(size=con_size, not_packed_rects=copy(config_rects), packed_rects=[], plot=False)
    if Configuration.plotting:
        update_temp_plot(C)
    packer = Packer(C)
    return packer.A1(C)



if __name__ == "__main__":
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
    
    rects = [Rect((0, 0), x[0], x[1], False) for x in cases]
    container_size = (20,20)
    C = Configuration(size=container_size, not_packed_rects=copy(rects), plot=False)
    if Configuration.plotting:
        initialize_plot(C, rects)
        update_temp_plot(C)
    packer = Packer(C)
    C = packer.A1(C)