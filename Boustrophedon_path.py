import numpy as np
import matplotlib.pyplot as plt
from Decomposition import Cell

def Boustrophedon_path(cell, horizontal_direction, vertical_direction, robot_radius, plot = False, color = None, width = None) :
    current_x = min(cell.min_x + robot_radius, cell.max_x)
    finish = False
    path = []
    while not finish :
        min_y = min(cell.floor[current_x] + robot_radius, cell.ceiling[current_x])
        max_y = max(cell.ceiling[current_x] - robot_radius, cell.floor[current_x])
        if vertical_direction == "UP" :
            path.append((current_x, min_y))
            path.append((current_x, max_y))
            vertical_direction = "DOWN"
        else :
            path.append((current_x, max_y))
            path.append((current_x, min_y))
            vertical_direction = "UP"
        if current_x + robot_radius < cell.max_x :
            next_x = min(current_x + robot_radius * 2, cell.max_x)
            for x in range(current_x + 1, next_x) :
                if vertical_direction == "UP" :
                    y = min(cell.floor[x] + robot_radius, cell.ceiling[x])
                else :
                    y = max(cell.ceiling[x] - robot_radius, cell.floor[x])
                path.append((x, y))
            current_x = next_x
        else :
            finish = True
    
    if horizontal_direction == "LEFT" :
        path.reverse()
    
    path_length = 0.0
    for i in range(1, len(path)) :
        A = np.asarray(path[i - 1])
        B = np.asarray(path[i])
        path_length += np.sqrt(np.sum((B - A) ** 2))

    start_point = path[0]
    end_point = path[-1]

    if plot :
        plt.plot(start_point[0], start_point[1], marker = 'o', color = 'orange', markersize = width + 6.4, zorder = 5)

        for i in range(len(path)) :
            if i == 0 or abs(path[i][1] - path[i - 1][1]) <= 1 :
                plt.plot(path[i][0], path[i][1], marker = 's', color = color, markersize = width, zorder = 2)
            else :
                # test case 1 : width + 1.6
                plt.plot([path[i - 1][0], path[i][0]], [path[i - 1][1], path[i][1]], color = color, linewidth = width + 1.6, zorder = 2)
        
        plt.plot(end_point[0], end_point[1], marker = 'X', color = 'mediumseagreen', markersize = width + 6.4, zorder = 5)

    return start_point, end_point, path_length