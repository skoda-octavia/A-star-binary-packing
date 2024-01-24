import matplotlib.pyplot as plt
from copy import copy
from matplotlib.patches import Rectangle as PltRect
from matplotlib.animation import FuncAnimation
import math
# Plot settings
PAUSE_TIME = 0.0001
placed_rect_color = 'lightblue'
unplaced_rect_color = 'grey'
edge_color = 'black'
alpha = 0.5


all_config_rects = []
rects = []
max_width_config = 0
max_width_global = 0

def argmax(lst):
    return lst.index(max(lst))


def clear_plot():
    global all_rects
    global max_width
    all_rects = []
    max_width = 0
    plt.clf()

def initialize_plot(C, all_rects, plot_size):
    global max_width_global
    global fig
    global axs
    global rects


    plt.ion()
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=plot_size)
    rects = all_rects
    max_width_global = sum([r.width for r in all_rects]) + 1 + len(all_rects)
    
    axs[1][0].set_xlim([0, C.width])
    axs[1][0].set_ylim([0, C.height])
    axs[1][0].set_xticks(range(0, C.width + 1, 5))
    axs[1][0].set_yticks(range(0, C.width + 1, 5))
    axs[1][1].set_title("Temp config")

    axs[0][0].set_xlim([0, C.width])
    axs[0][0].set_ylim([0, C.height])
    axs[0][0].set_xticks(range(0, C.width + 1, 5))
    axs[0][0].set_yticks(range(0, C.width + 1, 5))
    axs[0][0].set_title("Best config")

    axs[1][1].set_xticks([])
    axs[1][1].set_yticks([])
    axs[1][1].set_title("Temp rects used")

    axs[0][1].set_xticks([])
    axs[0][1].set_yticks([])
    axs[0][1].set_title("Rects used")
    

def equals(a: float, b: float) -> bool:
    tolerance = 1e-10
    return math.isclose(a, b, abs_tol=tolerance)


def set_temp_config(C, rects):
    global all_config_rects
    all_config_rects = rects

def update_temp_plot(C):
    global max_width_global
    global all_config_rects
    global axs

    max_width_config = sum([r.width for r in all_config_rects]) + 1 + len(all_config_rects)
    axs[1][0].clear()
    axs[1][1].clear()

    axs[1][0].set_xlim([0, C.width])
    axs[1][0].set_ylim([0, C.height])
    axs[1][0].set_xticks(range(0, C.width + 1, 5))
    axs[1][0].set_yticks(range(0, C.width + 1, 5))
    axs[1][0].set_title("Temp configuration")
    

    axs[1][1].set_xticks([])
    axs[1][1].set_yticks([])
    axs[1][1].set_xlim([0, max_width_global /2])
    axs[1][1].set_ylim([0, max_width_global /2])
    axs[1][1].set_title("Temp rects used")

    for rect in C.packed_rects:
        draw_rect(axs[1][0], (rect.placed_x, rect.placed_y), rect.width, rect.height, placed_rect_color, edge_color, alpha)

    draw_rects_overview(axs[1][1], all_config_rects, C.packed_rects, max_width_config)
    plt.draw()
    plt.pause(PAUSE_TIME)

def update_gloabl_plot(C):
    global max_width_global
    global rects 
    global axs

    max_width_global = sum([r.width for r in rects]) + 1 + len(rects)
    axs[0][0].clear()
    axs[0][1].clear()
    axs[0][0].set_xlim([0, C.width])
    axs[0][0].set_ylim([0, C.height])
    axs[0][0].set_xticks(range(0, C.width + 1, 5))
    axs[0][0].set_yticks(range(0, C.width + 1, 5))
    axs[0][0].set_title(f"Best configuration found: {len(C.packed_rects)}/{len(rects)}")

    axs[0][1].set_xticks([])
    axs[0][1].set_yticks([])
    axs[0][1].set_xlim([0, max_width_global / 2])
    axs[0][1].set_ylim([0, max_width_global / 2])
    axs[0][1].set_title("Rects used")

    for rect in C.packed_rects:
        draw_rect(axs[0][0], (rect.placed_x, rect.placed_y), rect.width, rect.height, placed_rect_color, edge_color, alpha)

    draw_rects_overview(axs[0][1], rects, C.packed_rects, max_width_global)
    plt.draw()
    plt.pause(PAUSE_TIME)


def draw_rects_overview(ax, all_rects: list, packed_rects: list, plot_max_width: float):
    tallest = 0
    current_pos = (1,1)
    rects_number = len(all_rects)
    placed = 0

    for rect in all_rects:
        w,h = rect.width, rect.height
        not_placed = True
        for packed_rect in packed_rects:
            if equals(packed_rect.width, w) and equals(packed_rect.height, h):
                not_placed = False
                break
            elif equals(packed_rect.width, h) and equals(packed_rect.height, w):
                not_placed = False
                break
        color = unplaced_rect_color if not_placed else placed_rect_color
        tallest = max(tallest, h)
        
        draw_rect(ax, current_pos, w, h, background_color=color, edge_color=edge_color,alpha=alpha)
        current_pos = (current_pos[0] + w + 1, current_pos[1])
        placed += 1

        if placed > math.sqrt(rects_number):
            current_pos = (1, current_pos[1] + tallest + 1)
            tallest = 0
            placed = 0

def freeze():
    plt.ioff()
    plt.show()

def draw_rect(ax, origin, w, h, background_color, edge_color, alpha):
    box = PltRect(origin, w, h, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)
