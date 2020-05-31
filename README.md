# Genetic Algorithm with modified operators for an integrated Traveling Salesman and Coverage Path Planning Problem
Coverage path planning (CPP) is a fundamental task to many robotics applications such as cleaning, mine sweeping, lawn mowing, UAV mapping and surveillance. One approach for a known environment with obstacles is to decompose the environment into cells such that each cell can be covered individually. We can then decide the visiting order of cells to connect those intra-cell paths together. Finding the shortest inter-cell path that visits every cell and returns to the origin cell is similar to the traveling salesman problem (TSP), the additional variation to consider is that there are multiple intra-cell path choices for each cell, those choices will result in different entry and exit points of cells, and therefore affect the inter-cell path. This integrated traveling salesman and coverage path planning problem is called TSP-CPP. Recent approaches for TSP-CPP include adapting dynamic programming algorithm for TSP, or brute force on combinations of entry and exit points of every cell and solve each entry and exit points combination with TSP-solver. Both of them suffer from exponential complexity and are prohibitive for complex environments with large number of cells. In this paper, we propose a genetic algorithm approach with modified operators for TSP-CPP. Our approach can find the same solution as the optimal solution of DP in all experiments. When cell number is large, our approach is more than one thousand times faster than DP approach. The proposed GA approach is also a potential solution for environments with cell number beyond the limit of DP.

### Boustrophedon cellular decomposition
![Boustrophedon cellular decomposition](https://github.com/WJTung/GA-TSPCPP/blob/master/1/decomposition.jpg)

### Visibility graph for finding the shortest path
![Visibility graph for finding the shortest path](https://github.com/WJTung/GA-TSPCPP/blob/master/1/visibility_example.jpg)

### Optimal solution
![Optimal solution](https://github.com/WJTung/GA-TSPCPP/blob/master/1/result.jpg)

### Random environments with multiple rectangular regions to cover
![Random environments with multiple rectangular regions to cover](https://github.com/WJTung/GA-TSPCPP/blob/master/random_map/21/1080_1080/01/GA_path.jpg)
