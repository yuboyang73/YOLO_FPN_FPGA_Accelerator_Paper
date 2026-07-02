/*
规模小
↓
便于手算和调试
↓
C Simulation / Cosim 更快
↓
先验证工具链，不追求性能
*/


#ifndef MATRIX_MULT_H
#define MATRIX_MULT_H

#define N 4

void matrix_mult(
    int A[N][N],
    int B[N][N],
    int C[N][N]
);

#endif