#include "matrix_mult.h"

void matrix_mult(
    int A[N][N],
    int B[N][N],
    int C[N][N]
) {
#pragma HLS INTERFACE s_axilite port=return
#pragma HLS INTERFACE s_axilite port=A
#pragma HLS INTERFACE s_axilite port=B
#pragma HLS INTERFACE s_axilite port=C

    Row :
    for (int i = 0; i < N; i++) {
    Col:
        for (int j = 0; j < N; j++) {
#pragma HLS PIPELINE II=1

            int sum = 0;

        Product:
            for (int k = 0; k < N; k++) {
                sum += A[i][k] * B[k][j];
            }

            C[i][j] = sum;
        }
    }
}