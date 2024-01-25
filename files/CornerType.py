from enum import Enum

class CornerType(Enum):
    TOP_RIGHT = 0   #    ########
    DOWN_RIGHT = 1  #    # ------  
    DOWN_LEFT = 2   #    #|  <- DOWN_RIGHT corner
    TOP_LEFT = 3    #    #|
    NONE = 4        #    #|