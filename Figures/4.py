# Different entry / exit points for cell 4 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import patches
import random
import pickle
from Redraw import *
from Decomposition import *
from Boustrophedon_path import *
from Visibility import *
import os

test_case = "1"

save_fig = 1

# variable
robot_radius = 10
cell_id_radius = 10 # outer circle for cell id
boundary_color = 'blue'
boundary_width = 2
intra_path_color = 'silver'
inter_path_color = 'dimgray'
path_width = 3.2

def display_cell(cell, cell_id) :
    # boundary
    
    for y in cell.left :
        plt.plot(cell.min_x, y, marker = 's', color = boundary_color, markersize = boundary_width, zorder = 1)
    
    for y in cell.right :
        plt.plot(cell.max_x, y, marker = 's', color = boundary_color, markersize = boundary_width, zorder = 1)
    
    ceiling_x = sorted(cell.ceiling)
    for i in range(len(ceiling_x)) :
        if i == 0 or abs(cell.ceiling[ceiling_x[i]] - cell.ceiling[ceiling_x[i - 1]]) <= 1 :
            plt.plot(ceiling_x[i], cell.ceiling[ceiling_x[i]], marker = 's', color = boundary_color, markersize = boundary_width, zorder = 1)
        else :
            plt.plot([ceiling_x[i - 1], ceiling_x[i]], [cell.ceiling[ceiling_x[i - 1]], cell.ceiling[ceiling_x[i]]], color = boundary_color, linewidth = boundary_width, zorder = 1)
    
    floor_x = sorted(cell.floor)
    for i in range(len(floor_x)) :
        if i == 0 or abs(cell.floor[floor_x[i]] - cell.floor[floor_x[i - 1]]) <= 1 :
            plt.plot(floor_x[i], cell.floor[floor_x[i]], marker = 's', color = boundary_color, markersize = boundary_width, zorder = 1)
        else :
            plt.plot([floor_x[i - 1], floor_x[i]], [cell.floor[floor_x[i - 1]], cell.floor[floor_x[i]]], color = boundary_color, linewidth = boundary_width, zorder = 1)

if __name__ == '__main__' :
    decomposed, total_cells_number, cells = pickle.load(open(test_case + "/decomposed_result", "rb"))

    min_x, max_x = 100, 220
    min_y, max_y = 100, 400
    my_dpi = 100

    direction_set = [("LEFT", "DOWN"), ("LEFT", "UP"), ("RIGHT", "DOWN"), ("RIGHT", "UP")]
    id = ['b', 'd', 'a', 'c']

    for i in range(4) :
        plt.close()

        fig = plt.figure(figsize = ((max_x - min_x) / my_dpi, (max_y - min_y) / my_dpi), dpi = my_dpi, frameon = False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        plt.xlim(min_x, max_x)
        plt.ylim(max_y, min_y) # invert y
        plt.gca().set_aspect('equal', adjustable = 'box')

        display_cell(cells[4], 4)
        
        direction = direction_set[i]
        start_point, end_point, _ = Boustrophedon_path(cells[4], direction[0], direction[1], robot_radius, plot = True, color = intra_path_color, width = path_width)

        arrow_color = 'green'
        arrow_width = 15
        if i == 0 or i == 3:
            dy = 1
            marker = 'v'
        else :
            dy = -1
            marker = '^'
        plt.plot([start_point[0], start_point[0]], [start_point[1] + dy * 20, start_point[1] + dy * 50], color = arrow_color, linewidth = path_width + 2, zorder = 3)
        plt.plot(start_point[0], start_point[1] + dy * 50, marker = marker, color = arrow_color, markersize = arrow_width, zorder = 3)
        plt.plot([end_point[0], end_point[0]], [end_point[1] - dy * 50, end_point[1] - dy * 20], color = arrow_color, linewidth = path_width + 2, zorder = 3)
        plt.plot(end_point[0], end_point[1] - dy * 20, marker = marker, color = arrow_color, markersize = arrow_width, zorder = 3)

        plt.savefig("entry_exit_example" + "_" + id[i] + ".jpg")
        # plt.show()
