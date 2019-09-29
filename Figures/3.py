# visibility graph example (not used in the paper)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.image as mpimg
from heapq import * 

# color, width : inter path
def shortest_path(test_case, start, goal, plot = False, color = None, width = None) :
    
    def visible(i, j) :
        A, B = vertices[i], vertices[j]
        for polygon_edge in polygon_edges :
            if i != polygon_edge[0] and i != polygon_edge[1] and j != polygon_edge[0] and j != polygon_edge[1] :
                C, D = vertices[polygon_edge[0]], vertices[polygon_edge[1]]
                if intersection(A, B, C, D) :
                    return False
        return True

    def distance(A, B) :
        return np.sqrt(np.sum((B - A) ** 2))

    # check if C is on AB
    def on_segment(A, B, P) :
        Ax, Ay, Bx, By, Px, Py = A[0], A[1], B[0], B[1], P[0], P[1]
        if min(Ax, Bx) <= Px and Px <= max(Ax, Bx) and min(Ay, By) <= Py and Py <= max(Ay, By) :
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
    
    vertices = list()
    polygon = list() # the polygon for corresponding vertex
    polygon_edges = list() # edge with vertex represented in index
    vertex_num = 0
    polygon_id = 1
    input = open(test_case + "/input.txt", "r")
    for line in input :
        L = (line.strip()).split(' ')
        cur_vertex_num = 0
        for i in range(0, len(L) - 1, 2) :
            vertex = (int(L[i]), int(L[i + 1])) # x, y
            vertices.append(vertex)
            cur_vertex_num = cur_vertex_num + 1
            polygon.append(polygon_id)
        for i in range(cur_vertex_num - 1) :
            polygon_edges.append((vertex_num + i, vertex_num + i + 1))
        polygon_edges.append((vertex_num + cur_vertex_num - 1, vertex_num))
        vertex_num = vertex_num + cur_vertex_num
        polygon_id = polygon_id + 1
    input.close()

    vertices.append(start)
    polygon.append('S')
    vertices.append(goal)
    polygon.append('G')
    start_index, goal_index = vertex_num, vertex_num + 1
    vertex_num = vertex_num + 2
    vertices = np.asarray(vertices)
    connected = np.zeros([vertex_num, vertex_num], dtype = bool)

    for polygon_edge in polygon_edges :
        connected[polygon_edge[0]][polygon_edge[1]] = True
        connected[polygon_edge[1]][polygon_edge[0]] = True

    for i in range(vertex_num) :
        for j in range(i + 1, vertex_num) :
            # not connected : not polygon edge, check connection 
            if (not connected[i][j]) and (polygon[i] != polygon[j]) and visible(i, j) :
                connected[i][j] = True
                connected[j][i] = True
                plt.plot([vertices[i][0], vertices[j][0]], [vertices[i][1], vertices[j][1]], color = 'silver', linewidth = width, zorder = 1)

    # Dijkstra
    Q = [] # cost, parent, vertex
    parent = np.full((vertex_num), -1, dtype = int)
    cost = np.full((vertex_num), np.inf, dtype = float)
    heappush(Q, (0, start_index, start_index))
    while Q and parent[goal_index] == -1 :
        (current_cost, p, u) = heappop(Q)
        if parent[u] == -1 :
            parent[u] = p
            cost[u] = current_cost
            for v in range(vertex_num) :
                if connected[u][v] and parent[v] == -1 :
                    heappush(Q, (current_cost + distance(vertices[u], vertices[v]), u, v))

    if plot : 
        cur_index = goal_index
        while cur_index != start_index :
            u, v = parent[cur_index], cur_index
            plt.plot([vertices[u][0], vertices[v][0]], [vertices[u][1], vertices[v][1]], color = color, linewidth = width, zorder = 2)
            cur_index = parent[cur_index]

    return cost[goal_index]

if __name__ == "__main__" :
    test_case = "1"
    start, goal = (58, 159), (601, 266) # points[9][1], points[29][0]
    color = 'dimgray'
    width = 3.2

    image = mpimg.imread(test_case + "/map.jpg")
    H, W = image.shape[0], image.shape[1]
    my_dpi = 100
    fig = plt.figure(figsize = (W / my_dpi, H / my_dpi), dpi = my_dpi, frameon = False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(image, aspect = "auto")

    plt.plot(start[0], start[1], marker = 'o', color = 'orange', markersize = width + 6.4, zorder = 3)
    plt.plot(goal[0], goal[1], marker = 'X', color = 'springgreen', markersize = width + 6.4, zorder = 3)

    print(shortest_path(test_case, start = start, goal = goal, plot = True, color = color, width = width))
    plt.savefig(test_case + "/visibility_example.jpg")