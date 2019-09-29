// usage : ./optimal test_case cell_num

#include <bits/stdc++.h>
using namespace std;

typedef vector <int> VI;
typedef vector <float> VF;
typedef vector <vector <float>> VVF;

VF intra_path_length;
VVF distance_matrix;

#define DISTANCE_MAX 1E10

int cell_num;

void rotation(VI &path) {
    // cycle : rotate path to start and end at cell 0
    int offset;
    bool reverse_order = false;
    for (int i = 0; i < cell_num; i++) {
        if (path[i] / 4 == 0) {
            offset = i;
            if (path[i] < 2) {
                reverse_order = true;
            }
        }
    }
    VI temp(cell_num);
    if (reverse_order) {
        for (int i = 0; i < cell_num; i++) {
            temp[i] = path[(offset - i + cell_num) % cell_num];
            int R = temp[i] % 4;
            if (R >= 2) {
                temp[i] -= 2;
            }
            else {
                temp[i] += 2;
            }
        }
    }
    else {
        for (int i = 0; i < cell_num; i++)
            temp[i] = path[(offset + i) % cell_num];
    }
    path.swap(temp);
    return;
}

float optimal_solution_from(VI &path, int start)
{
    // start : city (cell_num - 1) index : (cell_num - 1) * 4 + 0 ~ 3
    int N = cell_num - 1;
    int visited_state_num = 1 << N;
    float **distance_sum = new float*[visited_state_num];
    for (int i = 0; i < visited_state_num; i++)
        distance_sum[i] = new float[4 * N];
    int **from = new int*[visited_state_num];
    for (int i = 0; i < visited_state_num; i++)
        from[i] = new int[4 * N];
    for (int visited_state = 1; visited_state < visited_state_num; visited_state++) {
        for (int i = 0; i < 4 * N; i++)
            distance_sum[visited_state][i] = DISTANCE_MAX;
        for (int i = 0; i < 4 * N; i++) {
            int city = i / 4;
            if (visited_state & (1 << city)) {
                int prev_state = visited_state ^ (1 << city);
                if (prev_state == 0)
                    distance_sum[visited_state][i] = intra_path_length[start] + distance_matrix[start][i]; // start from i (start -> i -> ... -> start)
                else {
                    for (int j = 0; j < 4 * N; j++) {
                        if (distance_sum[prev_state][j] < DISTANCE_MAX) {
                            float cur_distance_sum = distance_sum[prev_state][j] + distance_matrix[j][i];
                            if (cur_distance_sum < distance_sum[visited_state][i]) {
                                distance_sum[visited_state][i] = cur_distance_sum;
                                from[visited_state][i] = j;
                            }
                        }
                    }
                }
                distance_sum[visited_state][i] += intra_path_length[i];
            }
        }
    }
    float min_distance = DISTANCE_MAX;
    int min_index = -1;
    for (int i = 0; i < 4 * N; i++) {
        distance_sum[(1 << N) - 1][i] += distance_matrix[i][start]; // cycle : back to start
        if (distance_sum[(1 << N) - 1][i] < min_distance) {
            min_distance = distance_sum[(1 << N) - 1][i];
            min_index = i;
        }
    }
    int cur = min_index, cur_state = (1 << N) - 1;
    for (int i = N - 1; i >= 0; i--) {
        path[i] = cur;
        cur = from[cur_state][path[i]];
        cur_state = cur_state ^ (1 << (path[i] / 4));
    }

    for (int i = 0; i < visited_state_num; i++)
        delete [] distance_sum[i];
    for (int i = 0; i < visited_state_num; i++)
        delete [] from[i];
    delete [] distance_sum;
    delete [] from;

    return min_distance;
}

// cycle : assume we always start and end at city N - 1
// try four possible entry / exit points of city N - 1
float optimal_solution(VI &path)
{
    int start_city = cell_num - 1;
    float min_distance = DISTANCE_MAX;
    for (int direction = 0; direction <= 3; direction++) {
        VI cur_path(cell_num);
        float distance = optimal_solution_from(cur_path, start_city * 4 + direction);
        cur_path[cell_num - 1] = start_city * 4 + direction;
        if (distance < min_distance) {
            min_distance = distance;
            path.swap(cur_path);
        }
    }
    return min_distance;
}

int main(int argc, char *argv[])
{
    string test_case(argv[1]);
    cell_num = atoi(argv[2]);
    
    string input_file = test_case + "/path_length.txt";
    string output_file = test_case + "/optimal.txt";
    
    // each city has 4 possible start point + end point combinations
    intra_path_length.resize(cell_num * 4);
    distance_matrix.assign(cell_num * 4, VF(cell_num * 4));

    ifstream input;
    input.open(input_file);

    for (int i = 0; i < cell_num * 4; i++)
        input >> intra_path_length[i];

    for (int i = 0; i < cell_num * 4; i++)
        for (int j = 0; j < cell_num * 4; j++)
            input >> distance_matrix[i][j];
    
    input.close();
    
    VI path(cell_num);
    float optimal = optimal_solution(path);
    cout << "Optimal Solution : " << optimal << '\n';
    
    rotation(path);
    ofstream output;
    output.open(output_file);
    output << optimal << '\n';
    for (int i = 0; i < (cell_num - 1); i++)
        output << path[i] << " -> ";
    output << path[cell_num - 1] << '\n';
}