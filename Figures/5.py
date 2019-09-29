# 0520 : example map for influence of entry / exit point and visiting order

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

test_case = "Figure3"
W, H = 480, 480

save_fig = 1
show_cell_id = 1

# variable
robot_radius = 10
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
        fontsize = 20, horizontalalignment = 'center', verticalalignment = 'center', zorder = 3)
    figure()

def display_cells(cells) :
    for cell_id in range(1, total_cells_number + 1) :
        cell = cells[cell_id]
        display_cell(cell, cell_id)

if __name__ == '__main__' : 
    decomposed, total_cells_number, cells = pickle.load(open(test_case + "/decomposed_result", "rb"))

    # show decomposed result
    decomposed_image = np.zeros([H, W, 3], dtype = np.uint8)
    decomposed_image[decomposed > 0, :] = [255, 255, 255] # white

    direction_set = [("LEFT", "DOWN"), ("LEFT", "UP"), ("RIGHT", "DOWN"), ("RIGHT", "UP")]
    # cities (start points, end points)
    points = np.zeros([4 * total_cells_number, 2, 2]) # 4 * total_cells_number city, start and end, x and y
    for cell_id in range(1, total_cells_number + 1) :
        for i in range(4) :
            direction = direction_set[i]
            start_point, end_point, _ = Boustrophedon_path(cells[cell_id], direction[0], direction[1], robot_radius)
            points[4 * (cell_id - 1) + i] = [start_point, end_point]

    visiting_order_list = ["2 -> 10 -> 14 -> 4", "2 -> 14 -> 4 -> 10", "2 -> 10 -> 14 -> 5"]

    plt.ion()

    for k in range(3) :
        plt.close()

        my_dpi = 100
        fig = plt.figure(figsize = (W / my_dpi, H / my_dpi), dpi = my_dpi, frameon = False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        plt.imshow(decomposed_image)
        ax.set_autoscale_on(False)
        
        display_cells(cells)

        direction_set = [("LEFT", "DOWN"), ("LEFT", "UP"), ("RIGHT", "DOWN"), ("RIGHT", "UP")]
        # cities (start points, end points)
        points = np.zeros([4 * total_cells_number, 2, 2]) # 4 * total_cells_number city, start and end, x and y
        for cell_id in range(1, total_cells_number + 1) :
            for i in range(4) :
                direction = direction_set[i]
                start_point, end_point, _ = Boustrophedon_path(cells[cell_id], direction[0], direction[1], robot_radius)
                points[4 * (cell_id - 1) + i] = [start_point, end_point]
        
        visiting_order = visiting_order_list[k].split(" -> ")
        
        total_length = 0.0
        for i in range(total_cells_number) :
            cell_id = int(int(visiting_order[i]) / 4) + 1
            direction = direction_set[int(visiting_order[i]) % 4]
            _, _, intra_path_length = Boustrophedon_path(cells[cell_id], direction[0], direction[1], robot_radius, plot = True, color = intra_path_color, width = path_width)
            # total_length += intra_path_length
            figure()
            total_length += shortest_path(test_case, start = points[int(visiting_order[i])][1], goal = points[int(visiting_order[(i + 1) % total_cells_number])][0], plot = True, color = inter_path_color, width = path_width) 
            figure()

        print(k + 1, ":", visiting_order, "total length =", total_length)

        if save_fig :
            plt.savefig("visiting_order_" + str(k + 1) + ".jpg")

'''
1 : ['2', '10', '14', '4'] total inter path length = 802.7755839892089
2 : ['2', '14', '4', '10'] total inter path length = 1347.4043681452542
3 : ['2', '10', '14', '5'] total inter path length = 991.361890956236
intra : 8512
'''