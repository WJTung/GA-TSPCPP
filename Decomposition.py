import numpy as np
import pickle
import matplotlib.image as mpimg

class Cell :
    def __init__(self) :
        self.min_x, self.max_x = None, None
        self.left, self.right = list(), list()
        self.ceiling, self.floor = dict(), dict()
        self.center = (None, None)

# 0 : obstacle (black), cell id = 1 ~ total_cells_number
def Boustrophedon_Cellular_Decomposition(test_case) :
    def calculate_connectivity(slice) :
        connectivity = 0
        connective_parts = []
        start_point = -1
        for i in range(len(slice)) :
            if slice[i] == 0 and start_point != -1 :
                connectivity += 1
                connective_parts.append((start_point, i))
                start_point = -1
            elif slice[i] == 1 and start_point == -1 :
                start_point = i
        if start_point != -1 :
            connectivity += 1
            connective_parts.append((start_point, len(slice)))
        return connectivity, connective_parts

    def get_adjacency_matrix(left_parts, right_parts) -> np.ndarray :
        adjacency_matrix = np.zeros([len(left_parts), len(right_parts)], dtype = bool)
        for i, left_part in enumerate(left_parts) :
            for j, right_part in enumerate(right_parts) :
                if min(left_part[1], right_part[1]) - max(left_part[0], right_part[0]) > 0:
                    adjacency_matrix[i, j] = True

        return adjacency_matrix

    def create_cells(decomposed, total_cells_number) :
        cells = [None] # there is no cell with cell id 0
        for cell_id in range(1, total_cells_number + 1) : 
            cell = Cell()
            cell.min_x, cell.max_x = W - 1, 0
            for y in range(H) :
                for x in range(W) :
                    if decomposed[y, x] == cell_id :
                        # update left
                        if x < cell.min_x :
                            cell.min_x, cell.left = x, [y]
                        elif x == cell.min_x :
                            cell.left.append(y)
                        # update right
                        if x > cell.max_x :
                            cell.max_x, cell.right = x, [y]
                        elif x == cell.max_x :
                            cell.right.append(y)
                        # update ceiling
                        if (x not in cell.ceiling) or (y > cell.ceiling[x]) :
                            cell.ceiling[x] = y
                        # update floor
                        if (x not in cell.floor) or (y < cell.floor[x]) :
                            cell.floor[x] = y

            x_center = int((cell.min_x + cell.max_x) / 2)
            y_center = int((cell.ceiling[x_center] + cell.floor[x_center]) / 2)
            cell.center = (x_center, y_center)

            cells.append(cell)
        
        return cells

    image = mpimg.imread(test_case + "/map.jpg")
    if len(image.shape) > 2 :
        image = image[:, :, 0]
    H, W = image.shape
    binary_image = (image > 127)

    last_connectivity = 0
    last_connectivity_parts = []
    last_cells = []
    total_cells_number = 0
    decomposed = np.zeros(binary_image.shape, dtype = int) # black

    for x in range(binary_image.shape[1]) :
        current_slice = binary_image[:, x]
        connectivity, connective_parts = calculate_connectivity(current_slice)

        if last_connectivity == 0 :
            current_cells = []
            for _ in range(connectivity) :
                total_cells_number += 1
                current_cells.append(total_cells_number)

        elif connectivity == 0 :
            current_cells = []
        
        else :
            adjacency_matrix = get_adjacency_matrix(last_connectivity_parts, connective_parts)
            current_cells = [0] * len(connective_parts)

            for i in range(last_connectivity) :
                if np.sum(adjacency_matrix[i, :]) == 1 :
                    for j in range(connectivity) :
                        if adjacency_matrix[i, j] :
                            current_cells[j] = last_cells[i]
                # IN
                elif np.sum(adjacency_matrix[i, :]) > 1 :
                    for j in range(connectivity) :
                        if adjacency_matrix[i, j] :
                            total_cells_number = total_cells_number + 1
                            current_cells[j] = total_cells_number

            for j in range(connectivity) :
                # OUT
                if np.sum(adjacency_matrix[:, j]) > 1 :
                    total_cells_number = total_cells_number + 1
                    current_cells[j] = total_cells_number
                # IN
                elif np.sum(adjacency_matrix[:, j]) == 0 :
                    total_cells_number = total_cells_number + 1
                    current_cells[j] = total_cells_number

        for cell, slice in zip(current_cells, connective_parts) :
            decomposed[slice[0] : slice[1], x] = cell

        last_connectivity = connectivity
        last_connectivity_parts = connective_parts
        last_cells = current_cells

    cells = create_cells(decomposed, total_cells_number)
    pickle.dump([decomposed, total_cells_number, cells], open(test_case + "/decomposed_result", "wb"))

if __name__ == "__main__" :
    test_case = "1"
    Boustrophedon_Cellular_Decomposition(test_case)