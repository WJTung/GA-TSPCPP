# redraw the map according to the vertex manually annotated on map_original.jpg
# map_original.jpg -> map.jpg

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.image as mpimg

def redraw(test_case, W, H) :
    input = open(str(test_case) + "/input.txt", "r")

    polygons = list()
    for line in input :
        L = (line.strip()).split(' ')
        polygon = list()
        for i in range(0, len(L) - 1, 2) :
            vertex = (int(L[i]), int(L[i + 1]))
            polygon.append(vertex)
        polygons.append(polygon)

    my_dpi = 100

    fig = plt.figure(figsize = (W / my_dpi, H / my_dpi), dpi = my_dpi, frameon = False)

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    image = np.full((H, W, 3), 255, dtype = np.uint8)
    ax.imshow(image, aspect = "auto")

    for polygon in polygons :
        ax.add_patch(patches.Polygon(polygon, color = "black"))

    fig.savefig(str(test_case) + "/map.jpg", dpi = my_dpi)

if __name__ == "__main__" :
    test_case = 7
    W, H = 1080, 1080
    redraw(test_case, W, H)
    plt.show()