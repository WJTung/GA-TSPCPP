// usage : ./GA test_case cell_num

#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#define x first
#define y second
#define DISTANCE_MAX 1E10

typedef std::vector<int> VI;
typedef std::vector<std::vector<int>> VVI;
typedef std::vector<float> VF;
typedef std::vector<std::vector<float>> VVF;

int cell_num;

const int population_size = 4096, max_generation = 16;
const float swap_mutation_probability = 0.02, crossover_probability = 0.9;

VVI population;
VF distance_sum;
VF prefix_sum; // for roulette wheel
VF intra_path_length;
VF difference;
VVF distance_matrix;

float best_distance_sum;
VI best_individual;

void swap(int& A, int& B) {
    int temp = A;
    A = B;
    B = temp;
    return;
}

float calculate_distance_sum(const VI& individual) {
    float D = 0.0;
    for (int i = 0; i < cell_num; ++i) {
        D += intra_path_length[individual[i]];
        if (i < (cell_num - 1)) {
            D += distance_matrix[individual[i]][individual[i + 1]];
        }
        else {
            D += distance_matrix[individual[cell_num - 1]][individual[0]];
        }
    }
    return D;
}

void update_distance_sum() {
    for (int i = 0; i < population_size; ++i) {
        distance_sum[i] = calculate_distance_sum(population[i]);
        if (distance_sum[i] < best_distance_sum) {
            best_distance_sum = distance_sum[i];
            best_individual = population[i];
        }
    }
    return;
}

void Knuth_shuffle(VI& A) {
    int N = A.size();
    for (int i = N - 1; i >= 1; --i) {
        int j = std::rand() % (i + 1);
        swap(A[i], A[j]);
    }
}

void initial_population() {
    for (int i = 0; i < population_size; ++i) {
        for (int j = 0; j < cell_num; ++j) {
            population[i][j] = j * 4 + (std::rand() % 4);
        }
        Knuth_shuffle(population[i]);
    }
}

void set_roulette_wheel() {
    fill(prefix_sum.begin(), prefix_sum.end(), 0.0);
    prefix_sum[0] = (1 / distance_sum[0]);
    for (int i = 1; i < population_size; ++i) {
        prefix_sum[i] = (prefix_sum[i - 1] + (1 / distance_sum[i]));
    }
    // normalize 
    for (int i = 0; i < population_size; ++i) { 
        prefix_sum[i] /= prefix_sum.back();
    }
}

int roulette_wheel_selection() {
    float R = std::rand() / (float)RAND_MAX;
    for (int i = 0; i < population_size; ++i) {
        if (R <= prefix_sum[i]) {
            return i;
        }
    }
    return std::rand() % population_size;
}

int find_index(const VI& individual, int cell) {
    for (int i = 0; i < cell_num; ++i) {
        if (individual[i] / 4 == cell) {
            return i;
        }
    }
    return -1;
}

VI heuristic_crossover(const VI &parent1, const VI &parent2) {
    VI offspring(cell_num);
    std::vector<bool> visited(cell_num, false);
    int start_cell = std::rand() % cell_num;
    visited[start_cell] = true;
    int left_index_1 = find_index(parent1, start_cell), right_index_1 = left_index_1;
    int left_index_2 = find_index(parent2, start_cell), right_index_2 = left_index_2;
    if (std::rand() % 2 == 0) {
        offspring[0] = parent1[left_index_1];
    } else {
        offspring[0] = parent2[left_index_2];
    }
    for (int i = 1; i < cell_num; ++i) {
        while (visited[parent1[left_index_1] / 4]) {
            left_index_1 = (left_index_1 - 1 + cell_num) % cell_num;
        }
        while (visited[parent1[right_index_1] / 4]) {
            right_index_1 = (right_index_1 + 1) % cell_num;
        }
        while (visited[parent2[left_index_2] / 4]) {
            left_index_2 = (left_index_2 - 1 + cell_num) % cell_num;
        }
        while (visited[parent2[right_index_2] / 4]) {
            right_index_2 = (right_index_2 + 1) % cell_num;
        }
        VI candidate_cells = {parent1[left_index_1] / 4, parent1[right_index_1] / 4, parent2[left_index_2] / 4, parent2[right_index_2] / 4};
        offspring[i] = candidate_cells[0] * 4 + 0;
        float cur_min = distance_matrix[offspring[i - 1]][offspring[i]] + difference[offspring[i]];
        for (int candidate_cell : candidate_cells) {
            for (int choice = 0; choice <= 3; ++choice) {
                int cell_path = candidate_cell * 4 + choice;
                float temp = distance_matrix[offspring[i - 1]][cell_path] + difference[cell_path];
                if (temp < cur_min) {
                    offspring[i] = cell_path;
                    cur_min = temp;
                }
            }
        }

        visited[offspring[i] / 4] = true;
    }
    return offspring;
}

void swap_mutation(VI& individual) {
    if (std::rand() % 100 <= (swap_mutation_probability * 100.0)) {
        int index1 = std::rand() % cell_num, index2 = std::rand() % cell_num;
        swap(individual[index1], individual[index2]);
    }
}

void best_choice_combination(VI& individual) {
    VI cell(cell_num);
    for (int i = 0; i < cell_num; ++i) {
        cell[i] = individual[i] / 4;
    }
    for (int starting_choice = 0; starting_choice < 4; starting_choice++) {
        std::vector<float> distance_sum(cell_num * 4, DISTANCE_MAX);
        std::vector<int> from(cell_num * 4, -1);
        int starting_cell_path = cell[0] * 4 + starting_choice;
        distance_sum[starting_cell_path] = intra_path_length[starting_cell_path];
        for (int i = 1; i < cell_num; ++i) {
            for (int choice = 0; choice < 4; ++choice) {
                int current_cell_path = cell[i] * 4 + choice;
                for (int previous_choice = 0; previous_choice < 4; ++previous_choice) {
                    int previous_cell_path = cell[i - 1] * 4 + previous_choice;
                    float cur_distance_sum = distance_sum[previous_cell_path] + distance_matrix[previous_cell_path][current_cell_path];
                    if (cur_distance_sum < distance_sum[current_cell_path]) {
                        distance_sum[current_cell_path] = cur_distance_sum;
                        from[current_cell_path] = previous_cell_path;
                    }
                }
                distance_sum[current_cell_path] += intra_path_length[current_cell_path];
            }
        }
        int best_ending_cell_path = -1;
        for (int ending_choice = 0; ending_choice < 4; ++ending_choice) {
            int ending_cell_path = cell[cell_num - 1] * 4 + ending_choice;
            distance_sum[ending_cell_path] += distance_matrix[ending_cell_path][starting_cell_path];
            if (best_ending_cell_path == -1 || distance_sum[ending_cell_path] < distance_sum[best_ending_cell_path]) {
                best_ending_cell_path = ending_cell_path;
            }
        }
        if (distance_sum[best_ending_cell_path] < calculate_distance_sum(individual)) {
            individual[cell_num - 1] = best_ending_cell_path;
            for (int i = cell_num - 1; i >= 1; --i) {
                individual[i - 1] = from[individual[i]];
            }
        }
    }
    return;
}

void evolve_next_generation() {
    VVI next_generation(population_size);
    set_roulette_wheel();

    for (int i = 0; i < population_size; ++i) {
        if (std::rand() % 100 <= (crossover_probability * 100.0)) {
            const VI& parent1 = population[roulette_wheel_selection()];
            const VI& parent2 = population[roulette_wheel_selection()];
            next_generation[i] = heuristic_crossover(parent1, parent2);
        }
        else {
            next_generation[i] = population[roulette_wheel_selection()];
        }
    }

    population.swap(next_generation);
    for (int i = 0; i < population_size; ++i) {
        swap_mutation(population[i]);
        best_choice_combination(population[i]);
    }
    update_distance_sum();
}

void rotation(VI &path) {
    // cycle : rotate path to start and end at cell 0
    int offset;
    bool reverse_order = false;
    for (int i = 0; i < cell_num; ++i) {
        if (path[i] / 4 == 0) {
            offset = i;
            if (path[i] < 2) {
                reverse_order = true;
            }
        }
    }
    VI temp(cell_num);
    if (reverse_order) {
        for (int i = 0; i < cell_num; ++i) {
            temp[i] = path[(offset - i + cell_num) % cell_num];
            int R = temp[i] % 4;
            if (R >= 2) {
                temp[i] -= 2;
            } else {
                temp[i] += 2;
            }
        }
    }
    else {
        for (int i = 0; i < cell_num; ++i) {
            temp[i] = path[(offset + i) % cell_num];
        }
    }
    path.swap(temp);
    return;
}

int main(int argc, char* argv[]) {
    std::string test_case(argv[1]);
    cell_num = atoi(argv[2]);

    std::string input_file = test_case + "/path_length.txt";
    std::string output_file = test_case + "/GA.txt";

    population.assign(population_size, VI(cell_num));
    distance_sum.resize(population_size);
    prefix_sum.resize(population_size); // for roulette wheel
    intra_path_length.resize(cell_num * 4);
    difference.resize(cell_num * 4);
    distance_matrix.assign(cell_num * 4, VF(cell_num * 4));

    best_distance_sum = DISTANCE_MAX;
    best_individual.resize(cell_num);

    {
        std::ifstream input;
        input.open(input_file);

        for (int i = 0; i < cell_num * 4; ++i) {
            input >> intra_path_length[i];
        }

        // each cell has 4 possible entry / exit points choices (4 cell-path combinations)
        for (int i = 0; i < cell_num * 4; ++i) {
            for (int j = 0; j < cell_num * 4; ++j) {
                input >> distance_matrix[i][j];
            }
        }
        
        input.close();
    }

    for (int i = 0; i < cell_num; ++i) {
        float min_intra_path_length = std::min(intra_path_length[i * 4 + 0], intra_path_length[i * 4 + 1]);
        for (int j = 0; j < 4; ++j) {
            difference[i * 4 + j] = intra_path_length[i * 4 + j] - min_intra_path_length;
        }
    }

    std::srand(2019);

    initial_population();
    update_distance_sum();
    
    for (int generation = 1; generation <= max_generation; ++generation) {
        evolve_next_generation();
        
        std::cout << "Generation " << generation << '\n';
        std::cout << "Best distance sum = " << best_distance_sum << '\n';
        std::cout << '\n';
    }
    
    std::cout << "GA : " << best_distance_sum << '\n';

    {
        rotation(best_individual);
        std::ofstream output;
        output.open(output_file);
        output << best_distance_sum << '\n';
        for (int i = 0; i < (cell_num - 1); ++i) {
            output << best_individual[i] << " -> ";
        }
        output << best_individual[cell_num - 1] << '\n';
        output.close();
    }
}
