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

# 1 : 640 * 480
# 2 : 1200 * 1200
# 3 : 1080 * 1080
# 4 : 1280 * 720
# 5 : 1080 * 1080
# Figure3 : 480 * 480
# 6 : 1080 * 1080

test_case = "6"
W, H = 1080, 1080

# option
# generate_decomposition, generate_distance_matrix, generate_visiting_order : only required for a new map
generate_map = 1
generate_decomposition = 1
generate_path_length = 1
generate_visiting_order = 1

save_fig = 1
show_cell_id = 1

# variable
robot_radius = 10
boundary_color = 'blue'
boundary_width = 2
intra_path_color = 'silver'
inter_path_color = 'dimgray'
if test_case == "1" :
    path_width = 3.2
    marker_size = 9.6
else :
    path_width = 5
    marker_size = 12

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
        plt.close()
    
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
    
    display_cells(cells)

    direction_set = [("LEFT", "DOWN"), ("LEFT", "UP"), ("RIGHT", "DOWN"), ("RIGHT", "UP")]
    # cities (start points, end points)
    points = np.zeros([4 * total_cells_number, 2, 2]) # 4 * total_cells_number city, start and end, x and y
    intra_path_length = np.zeros([4 * total_cells_number])
    for cell_id in range(1, total_cells_number + 1) :
        for i in range(4) :
            direction = direction_set[i]
            start_point, end_point, path_length = Boustrophedon_path(cells[cell_id], direction[0], direction[1], robot_radius)
            points[4 * (cell_id - 1) + i] = [start_point, end_point]
            intra_path_length[4 * (cell_id - 1) + i] = path_length
    
    if generate_path_length : 
        # generating distance matrix
        output_file = open(test_case + "/path_length.txt", "w")
        
        # intra path length
        for i in range(4 * total_cells_number) :
            print(round(intra_path_length[i], 8), end = ' ', file = output_file)
        print(file = output_file)
        
        # distance matrix
        distance_matrix = np.zeros([4 * total_cells_number, 4 * total_cells_number])
        for i in range(4 * total_cells_number) :
            for j in range(4 * total_cells_number) :
                distance_matrix[i][j] = shortest_path(test_case, start = points[i][1], goal = points[j][0], plot = False)
                print(round(distance_matrix[i][j], 8), end = ' ', file = output_file)
            print(file = output_file)
        
        output_file.close()

    if generate_visiting_order :
        os.system("./optimal " + test_case + " " + str(total_cells_number))

    optimal_output = open(test_case + "/optimal.txt")
    optimal_length = float(optimal_output.readline().rstrip())
    visiting_order = optimal_output.readline().rstrip()
    visiting_order = visiting_order.split(" -> ")
    
    for i in range(total_cells_number) :
        cell_id = int(int(visiting_order[i]) / 4) + 1
        direction = direction_set[int(visiting_order[i]) % 4]

        if test_case == "1" : 
            Boustrophedon_path(cells[cell_id], direction[0], direction[1], robot_radius, plot = True, color = intra_path_color, width = path_width)
        else :
            start_point, end_point = points[int(visiting_order[i])][0], points[int(visiting_order[i])][1]
            plt.plot(start_point[0], start_point[1], marker = 'o', color = 'orange', markersize = marker_size, zorder = 5)
            plt.plot(end_point[0], end_point[1], marker = 'X', color = 'mediumseagreen', markersize = marker_size, zorder = 5)
        figure()
        
        shortest_path(test_case, start = points[int(visiting_order[i])][1], goal = points[int(visiting_order[(i + 1) % total_cells_number])][0], plot = True, color = inter_path_color, width = path_width) 
        figure()

    if save_fig :
        plt.savefig("result" + test_case + ".jpg")