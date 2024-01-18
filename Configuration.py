from Rectangle import Rectangle as Rect
from copy import deepcopy, copy
from CornerType import CornerType
from Plot import initialize_plot, plot_configuration


class Configuration:

    def __init__(self, size: tuple[float], not_packed_rects: list[Rect] = [], packed_rects: list[Rect] = []) -> None:
        self.set_size(size)
        self.not_packed_rects = not_packed_rects
        self.packed_rects = packed_rects
        self.containing_distance = 0.2
        self.generate_L()
        initialize_plot(self)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


    def set_size(self, size: tuple[float]) -> None:
        if len(size) != 2 or size[0] < 0 or size[1] < 0:
            raise ValueError("Invalid size args", size)
        else:
            self.width = size[0]
            self.height = size[1]


    def generate_L(self):
        ccoas = []
        possible_corners = self.get_possible_corners()
        for not_packed_rect in self.not_packed_rects:
            width, height = not_packed_rect.width, not_packed_rect.height
            for corner, corner_type in possible_corners:
                for rotated in [False, True]:
                    ccoa = Rect(corner, width, height, rotated, corner_type)
                    if self.rect_fits(ccoa, corner_type):
                        ccoas.append(ccoa)
        self.L = ccoas
    

    def get_possible_corners(self) -> list[tuple[tuple, CornerType]]:
        possible_corners = []
        for corner in self.get_all_corners():
            cor_type = self.get_corner_type(corner)
            if cor_type != CornerType.NONE:
                possible_corners.append((corner, cor_type))     
        return possible_corners


    def get_all_corners(self) -> list[tuple]:
        corners = []
        for rect in self.packed_rects:
            corners.append((rect.placed_x, rect.placed_y))
            corners.append((rect.placed_x + rect.width, rect.placed_y))
            corners.append((rect.placed_x, rect.placed_y + rect.height))
            corners.append((rect.placed_x + rect.width, rect.placed_y + rect.height))
        corners.append((0, 0))
        corners.append((0, self.height))
        corners.append((self.width, 0))
        corners.append((self.width, self.height))
        return corners
    

    def get_corner_type(self, corner: tuple[float, float]) -> CornerType:
        north_east = corner[0] + self.containing_distance, corner[1] + self.containing_distance
        south_east = corner[0] - self.containing_distance, corner[1] + self.containing_distance
        south_west = corner[0] - self.containing_distance, corner[1] - self.containing_distance
        north_west = corner[0] + self.containing_distance, corner[1] - self.containing_distance
        taken_list = []
        taken_list.append(self.point_taken(north_east))
        taken_list.append(self.point_taken(south_east))
        taken_list.append(self.point_taken(south_west))
        taken_list.append(self.point_taken(north_west))
        if sum(taken_list) == 3: # corner
            index = taken_list.index(False)
            return CornerType(index)
        else:
            return CornerType.NONE


    def point_taken(self, point: tuple[float, float]) -> bool:
        if point[0] < 0 or point[0] > self.width or point[1] < 0 or point[1] > self.height:
            return True
        
        for rect in self.packed_rects:
            if rect.contains_point(point):
                return True
        return False

    def rect_fits(self, ccoa: Rect, corner_type: CornerType) -> bool:
        for rect in self.packed_rects:
            if rect.overlaps(ccoa):
                return False
        
        if ccoa.top_y > self.height or ccoa.placed_y < 0:
            return False
        if ccoa.top_x > self.width or ccoa.placed_x < 0:
            return False
        return True


    def place_rect(self, rect: Rect) -> None:
        #TODO removing from ccoas
        self.packed_rects.append(rect)

        for not_packed_rect in self.not_packed_rects:
            if Rect.equals(rect.width, not_packed_rect.width) and Rect.equals(rect.height, not_packed_rect.height):
                self.not_packed_rects.remove(not_packed_rect)
                break
            elif Rect.equals(rect.width, not_packed_rect.height) and Rect.equals(rect.height, not_packed_rect.width):
                self.not_packed_rects.remove(not_packed_rect)
                break
        self.generate_L()

        plot_configuration(self, self.successful())


    def density(self) -> float:
        container_area = self.height * self.width
        occupied_areas = [rect.height * rect.width for rect in self.packed_rects]
        return container_area/sum(occupied_areas)
    
    def successful(self) -> bool:
        return len(self.not_packed_rects) == 0
    