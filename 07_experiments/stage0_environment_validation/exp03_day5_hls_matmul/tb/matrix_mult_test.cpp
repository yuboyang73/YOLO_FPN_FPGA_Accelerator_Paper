#include <iostream>
#include "D:\.YOLO_FPN_FPGA_Accelerator_Paper\07_experiments\stage0_environment_validation\exp03_day5_hls_matmul\src\matrix_mult.h"

using namespace std;

int main() {
    int A[N][N] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {1, 1, 1, 1},
        {2, 2, 2, 2}
    };

    int B[N][N] = {
        {1, 0, 0, 0},
        {0, 1, 0, 0},
        {0, 0, 1, 0},
        {0, 0, 0, 1}
    };

    int C[N][N] = {0};

    matrix_mult(A, B, C);

    cout << "Result C:" << endl;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            cout << C[i][j] << " ";
        }
        cout << endl;
    }

    bool pass = true;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (C[i][j] != A[i][j]) {
                pass = false;
            }
        }
    }

    if (pass) {
        cout << "TEST PASSED" << endl;
        return 0;
    } else {
        cout << "TEST FAILED" << endl;
        return 1;
    }
}