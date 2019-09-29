import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from Boustrophedon_path import *
import os
import pickle

rectangle_num = 21

min_length, max_length = 64, 256
map_W, map_H = 1080, 1080
radius = 16

# check if C is on AB
def on_segment(A, B, P) :
    Ax, Ay, Bx, By, Px, Py = A[0], A[1], B[0], B[1], P[0], P[1]
    if min(Ax, Bx) <= Px + 1E-6 and Px <= max(Ax, Bx) + 1E-6 and min(Ay, By) <= Py + 1E-6 and Py <= max(Ay, By) + 1E-6 :
        return True
    return False

# AB CD
def intersection(A, B, C, D) :
    Ax, Ay, Bx, By, Cx, Cy, Dx, Dy = A[0], A[1], B[0], B[1], C[0], C[1], D[0], D[1]
    # m1 = m2
    if (Ay - By) * (Cx - Dx) == (Cy - Dy) * (Ax - Bx) :
        return False
    # m1 = inf, x = Ax
    if Ax == Bx : 
        m2 = (Cy - Dy) / (Cx - Dx)
        b2 = Cy - m2 * Cx
        P = (Ax, m2 * Ax + b2)
    # m2 = inf, x = Cx
    elif Cx == Dx : 
        m1 = (Ay - By) / (Ax - Bx)
        b1 = Ay - m1 * Ax
        P = (Cx, m1 * Cx + b1)
    else :
        m1 = (Ay - By) / (Ax - Bx)
        b1 = Ay - m1 * Ax
        m2 = (Cy - Dy) / (Cx - Dx)
        b2 = Cy - m2 * Cx
        Px = (b1 - b2) / (m2 - m1)
        Py = m1 * Px + b1
        P = (Px, Py)
    if on_segment(A, B, P) and on_segment(C, D, P) :
        return True
    return False

def dot(A, B) :
    return A[0] * B[0] + A[1] * B[1]

def vector(A, B) :
    return (B[0] - A[0], B[1] - A[1])

def inside_rectangle(point, rectangle) :
    # https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
    A = rectangle[0]
    B = rectangle[1]
    C = rectangle[2]
    M = point
    if (0 < dot(vector(A, B), vector(A, M)) and
            dot(vector(A, B), vector(A, M)) < dot(vector(A, B), vector(A, B)) and
            0 < dot(vector(B, C), vector(B, M)) and
            dot(vector(B, C), vector(B, M)) < dot(vector(B, C), vector(B, C))) :
        return True
    return False

def inside_rectangles(point, rectangles) :
    for rectangle in rectangles :
        if inside_rectangle(point, rectangle) :
            return True
    return False

def inside_map(point) :
    return (0 < point[0] and point[0] < map_W and 0 < point[1] and point[1] < map_H)

def no_edges_intersection(edges, new_edges) :
    for edge in edges :
        for new_edge in new_edges :
            if intersection(edge[0], edge[1], new_edge[0], new_edge[1]) :
                return False
    return True

my_dpi = 100

direction_set = [("LEFT", "DOWN"), ("LEFT", "UP"), ("RIGHT", "DOWN"), ("RIGHT", "UP")]

np.random.seed(2019)

os.mkdir(str(rectangle_num) + "/" + str(map_W) + "_" + str(map_H))

for T in range(10) :
    test_case = str(rectangle_num) + "/" + str(map_W) + "_" + str(map_H) + "/" + str(T + 1).zfill(2)

    rectangles = []
    edges = []

    rotated_paths = []
    start_points = []
    end_points = []
    path_lengths = []

    for num in range(1, rectangle_num + 1) :
        feasible = False
        while not feasible :
            inside = True
            while inside :
                A = (np.random.randint(0, map_W), np.random.randint(0, map_H))
                inside = inside_rectangles(A, rectangles)
            rectangle_W, rectangle_H = np.random.randint(min_length / (radius * 2), (max_length + 1) / (radius * 2)) * (radius * 2), np.random.randint(min_length, max_length + 1)
            theta = np.random.rand() * 2 * np.pi
            # https://en.wikipedia.org/wiki/Rotation_matrix
            B = (A[0] + rectangle_W * np.cos(theta), A[1] + rectangle_W * np.sin(theta))
            C = (A[0] + rectangle_W * np.cos(theta) - rectangle_H * np.sin(theta), 
                    A[1] + rectangle_W * np.sin(theta) + rectangle_H * np.cos(theta))
            D = (A[0] - rectangle_H * np.sin(theta), A[1] + rectangle_H * np.cos(theta))
            if inside_map(B) and inside_map(C) and inside_map(D) :
                new_edges = [(A, B), (B, C), (C, D), (D, A)]
                feasible = no_edges_intersection(edges, new_edges)
                for rectangle in rectangles :
                    if inside_rectangle(rectangle[0], [A, B, C]) :
                        feasible = False

        for direction in direction_set :
            path, path_length = Boustrophedon_path(rectangle_W, rectangle_H, direction[0], direction[1], radius)
            rotated_path = []
            for node in path :
                x = A[0] + node[0] * np.cos(theta) - node[1] * np.sin(theta)
                y = A[1] + node[0] * np.sin(theta) + node[1] * np.cos(theta)
                rotated_path.append((x, y))
            
            rotated_paths.append(rotated_path)
            start_points.append(rotated_path[0])
            end_points.append(rotated_path[-1])
            path_lengths.append(path_length)
        
        edges = edges + new_edges
        rectangle = [A, B, C, D, rectangle_W, rectangle_H, theta]
        rectangles.append(rectangle)

    os.mkdir(test_case)

    pickle.dump(rectangles, open(test_case + "/rectangles", "wb"))

    output_file = open(test_case + "/path_length.txt", "w")

    # intra path length
    for i in range(4 * rectangle_num) :
        print(round(path_lengths[i], 8), end = ' ', file = output_file)
    print(file = output_file)

    # distance matrix
    distance_matrix = np.zeros([4 * rectangle_num, 4 * rectangle_num])
    for i in range(4 * rectangle_num) :
        for j in range(4 * rectangle_num) :
            start = np.asarray(end_points[i])
            goal = np.asarray(start_points[j])
            distance_matrix[i][j] = np.sqrt(np.sum((goal - start) ** 2))
            print(round(distance_matrix[i][j], 8), end = ' ', file = output_file)
        print(file = output_file)

    output_file.close()

    os.system("./optimal " + test_case + " " + str(rectangle_num))
    os.system("./GA " + test_case + " " + str(rectangle_num))

    optimal_output = open(test_case + "/optimal.txt")
    optimal_length = float(optimal_output.readline().rstrip())
    optimal_visiting_order = optimal_output.readline().rstrip()
    optimal_visiting_order = optimal_visiting_order.split(" -> ")

    GA_output = open(test_case + "/GA.txt")
    GA_length = float(GA_output.readline().rstrip())
    GA_visiting_order = GA_output.readline().rstrip()
    GA_visiting_order = GA_visiting_order.split(" -> ")

    result_file = open(test_case + "/result.txt", "w")
    print((GA_length - optimal_length) / optimal_length * 100.0, '%', file = result_file)
    print(optimal_length, GA_length, file = result_file)
    result_file.close()

    for k in range(2) :
        if k == 0 :
            visiting_order = optimal_visiting_order
        else :
            visiting_order = GA_visiting_order
        
        plt.close()
        fig = plt.figure(figsize = (map_W / my_dpi, map_H / my_dpi), dpi = my_dpi, frameon = False)

        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        image = np.full((map_H, map_W, 3), 255, dtype = np.uint8)
        ax.imshow(image, aspect = "auto")
        
        for i in range(rectangle_num) :
            rectangle = rectangles[i]
            ax.add_patch(patches.Polygon(rectangle[0 : 4], color = "lightgray"))
            center = ((rectangle[0][0] + rectangle[2][0]) / 2, (rectangle[0][1] + rectangle[2][1]) / 2)
            plt.text(center[0], center[1], str(i + 1), color = 'blue', weight = 'bold',
            fontsize = 20, horizontalalignment = 'center', verticalalignment = 'center', zorder = 2)

        for i in range(rectangle_num) :
            cell_path = int(visiting_order[i])
            cell_id = int(cell_path / 4) + 1
            direction = direction_set[cell_path % 4]

            start_point = start_points[cell_path]
            end_point = end_points[cell_path]
            rotated_path = rotated_paths[cell_path]

            plt.plot(start_point[0], start_point[1], marker = 'o', color = 'orange', markersize = 12.8, zorder = 4)

            for j in range(1, len(rotated_path)) :
                plt.plot([rotated_path[j - 1][0], rotated_path[j][0]], [rotated_path[j - 1][1], rotated_path[j][1]], color = "dimgray", linewidth = 6.4, zorder = 2)
                
            plt.plot(end_point[0], end_point[1], marker = 'X', color = 'mediumseagreen', markersize = 12.8, zorder = 4)

            next_start_point = start_points[int(visiting_order[(i + 1) % rectangle_num])]
            plt.plot([end_point[0], next_start_point[0]], [end_point[1], next_start_point[1]], color = "black", linewidth = 6.4, zorder = 3)
        
        if k == 0 :
            plt.savefig(test_case + "/optimal_path.jpg")
        else :
            plt.savefig(test_case + "/GA_path.jpg")