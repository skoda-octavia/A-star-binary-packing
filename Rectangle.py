import math
from CornerType import CornerType
from copy import deepcopy

class Rectangle:

    def __init__(self, placed: tuple, width: float, height: float, rotated: bool, corner_type: CornerType=CornerType.NONE) -> None:
        self.set_width_height(width, height, rotated)
        self.set_placed(placed, rotated, corner_type)
        self.set_tops()

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

    def set_tops(self) -> None:
        self.top_x = self.placed_x + self.width
        self.top_y = self.placed_y + self.height

    @staticmethod
    def equals(a: float, b: float) -> bool:
        tolerance = 1e-10
        return math.isclose(a, b, abs_tol=tolerance)


    def set_placed(self, placed: tuple, rotated: bool, corner_type: CornerType) -> None:
        if len(placed) != 2:
            raise ValueError("Placed arg not len of 2", placed)
        self.placed_x = placed[0]
        self.placed_y = placed[1]
        if corner_type == CornerType.DOWN_LEFT or corner_type == CornerType.DOWN_RIGHT:
            self.placed_y = placed[1] - self.height
        if corner_type == CornerType.TOP_LEFT or corner_type == CornerType.DOWN_LEFT:
            self.placed_x = placed[0] - self.width


    def set_width_height(self, width: float, height: float, rotated: bool) -> None:
        if width < 0 or height < 0:
            raise ValueError("Negative rect height or width", width, height)
        if rotated:
            self.width = height
            self.height = width
        else:
            self.width = width
            self.height = height


    def min_distance_from(self, other):
        vertical_dis = self.vertical_distance(other)
        horizontal_dis = self.horizontal_distance(other)
        return math.sqrt(vertical_dis**2 + horizontal_dis**2)

    def vertical_distance(self, other) -> float:
        if self.top_y < other.placed_y:
            return other.placed_y - self.top_y
        elif other.top_y < self.placed_y:
            return self.placed_y - other.top_y
        else:
            return 0
        
    def horizontal_distance(self, other):
        if self.top_x < other.placed_x:
            return other.placed_x - self.top_x
        elif other.top_x < self.placed_x:
            return self.placed_x - other.top_x
        else:
            return 0
        
    def contains_point(self, point: tuple[float, float]) -> bool:
        if point[0] > self.placed_x and point[0] < self.top_x:
            return True
        if point[1] > self.placed_y and point[1] < self.top_y:
            return True
        return False
    
    def overlaps(self, other):
        if self.top_y < other.placed_y or self.placed_y > other.top_y:
            return False
        if self.top_x < other.placed_x or self.placed_x > other.top_x:
            return False
        return True