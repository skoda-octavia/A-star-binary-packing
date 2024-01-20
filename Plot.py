import matplotlib.pyplot as plt
from copy import copy
from matplotlib.patches import Rectangle as PltRect
from matplotlib.animation import FuncAnimation
import math
# Plot settings
PLOT = True
placed_rect_color = 'lightblue'
unplaced_rect_color = 'grey'
edge_color = 'black'
alpha = 0.5


all_rects = []
max_width = 0

def argmax(lst):
    return lst.index(max(lst))

def initialize_plot(C, rects, plot_size = (12,6)):
    global max_width
    global all_rects
    global fig
    global axs

    plt.ion()
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=plot_size)
    all_rects = rects
    max_width = sum([r.width for r in all_rects]) + 1 + len(all_rects)
    axs[0].set_xlim([0, C.width])
    axs[0].set_ylim([0, C.height])
    axs[0].set_xticks(range(0, C.width + 1, 5))
    axs[0].set_yticks(range(0, C.width + 1, 5))

    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_xlim([0, max_width])
    axs[1].set_ylim([0, max_width])


def equals(a: float, b: float) -> bool:
    tolerance = 1e-10
    return math.isclose(a, b, abs_tol=tolerance)

def update_plot(C):
    global max_width
    global all_rects
    global axs

    max_width = sum([r.width for r in all_rects]) + 1 + len(all_rects)
    axs[0].clear()
    axs[1].clear()
    axs[0].set_xlim([0, C.width / 2])
    axs[0].set_ylim([0, C.height /2])
    axs[0].set_xticks(range(0, C.width + 1, 5))
    axs[0].set_yticks(range(0, C.width + 1, 5))

    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_xlim([0, max_width / 2])
    axs[1].set_ylim([0, max_width / 2])

    for rect in C.packed_rects:
        draw_rect(axs[0], (rect.placed_x, rect.placed_y), rect.width, rect.height, placed_rect_color, edge_color, alpha)

    draw_rects_overview(axs[1], all_rects, C.not_packed_rects)
    plt.draw()
    plt.pause(0.005)



def draw_rects_overview(ax, all_rects: list, not_placed_rects: list):
    tallest = 0
    current_pos = (1,1)

    for rect in all_rects:
        w,h = rect.width, rect.height
        not_placed = False
        for not_placed_rect in not_placed_rects:
            if equals(not_placed_rect.width, w) and equals(not_placed_rect.height, h):
                not_placed = True
                break
            elif equals(not_placed_rect.width, h) and equals(not_placed_rect.height, w):
                not_placed = True
                break
        color = unplaced_rect_color if not_placed else placed_rect_color
        tallest = max(tallest, h)
        
        draw_rect(ax, current_pos, w, h, background_color=color, edge_color=edge_color,alpha=alpha)
        current_pos = (current_pos[0] + w + 1, current_pos[1])
        
        if max_width / 3 < current_pos[0] + w + 1:
            current_pos = (1, current_pos[1] + tallest + 1)
            tallest = 0


def draw_rect(ax, origin, w, h, background_color, edge_color, alpha):
    box = PltRect(origin, w, h, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)
