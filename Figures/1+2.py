# 1 : Decomposition
# 2 : Boustrophedon path : intra path example

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
W, H = 640, 480

# option
# generate_decomposition, generate_distance_matrix, generate_visiting_order : only required for a new map
generate_map = 0
generate_decomposition = 0

save_fig = 1
show_cell_id = 1

# variable
robot_radius = 10
cell_id_radius = 10 # outer circle for cell id
boundary_color = 'blue'
boundary_width = 2
intra_path_color = 'silver'
inter_path_color = 'dimgray'
path_width = 3.2

def figure() :
    if not save_fig :
        plt.pause(0.5)

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
    
    if show_cell_id :
        # id
        plt.text(cell.center[0] + 0.5, cell.center[1] + 0.5, str(cell_id), color = 'brown', weight = 'bold',
        fontsize = 18, horizontalalignment = 'center', verticalalignment = 'center', zorder = 3)
    figure()

def display_cells(cells) :
    for cell_id in range(1, total_cells_number + 1) :
        cell = cells[cell_id]
        display_cell(cell, cell_id)

if __name__ == '__main__' :
    if generate_map :
        redraw(test_case, W, H)
    
    if generate_decomposition :
        Boustrophedon_Cellular_Decomposition(test_case)
    
    decomposed, total_cells_number, cells = pickle.load(open(test_case + "/decomposed_result", "rb"))

    plt.ion()

    my_dpi = 100
    fig = plt.figure(figsize = (W / my_dpi, H / my_dpi), dpi = my_dpi, frameon = False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # show decomposed result
    decomposed_image = np.zeros([H, W, 3], dtype = np.uint8)
    decomposed_image[decomposed > 0, :] = [255, 255, 255] # white
    plt.imshow(decomposed_image)
    ax.set_autoscale_on(False)
    
    # decomposition result
    display_cells(cells)
    if save_fig :
        plt.savefig("decomposition.jpg")

    # intra example
    for cell_id in range(1, total_cells_number + 1) :
        Boustrophedon_path(cells[cell_id], "RIGHT", "DOWN", robot_radius, plot = True, color = intra_path_color, width = path_width)
        figure()
    if save_fig :
        plt.savefig("intra_example.jpg")