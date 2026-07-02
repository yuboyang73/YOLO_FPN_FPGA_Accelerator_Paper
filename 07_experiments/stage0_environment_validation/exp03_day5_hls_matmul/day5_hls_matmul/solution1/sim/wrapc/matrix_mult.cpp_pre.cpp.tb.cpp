// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.2 (64-bit)
// Tool Version Limit: 2019.12
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// ==============================================================
# 1 "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/src/matrix_mult.cpp"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/src/matrix_mult.cpp"
# 1 "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/src/matrix_mult.h" 1
# 17 "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/src/matrix_mult.h"
void matrix_mult(
    int A[4][4],
    int B[4][4],
    int C[4][4]
);
# 2 "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/src/matrix_mult.cpp" 2

void matrix_mult(
    int A[4][4],
    int B[4][4],
    int C[4][4]
) {
#pragma HLS INTERFACE s_axilite port=return
#pragma HLS INTERFACE s_axilite port=A
#pragma HLS INTERFACE s_axilite port=B
#pragma HLS INTERFACE s_axilite port=C

    Row :
    for (int i = 0; i < 4; i++) {
    Col:
        for (int j = 0; j < 4; j++) {
#pragma HLS PIPELINE II=1

            int sum = 0;

        Product:
            for (int k = 0; k < 4; k++) {
                sum += A[i][k] * B[k][j];
            }

            C[i][j] = sum;
        }
    }
}
#ifndef HLS_FASTSIM
#ifdef __cplusplus
extern "C"
#endif
void apatb_matrix_mult_ir(int (*)[4], int (*)[4], int (*)[4]);
#ifdef __cplusplus
extern "C"
#endif
void matrix_mult_hw_stub(int (*A)[4], int (*B)[4], int (*C)[4]){
matrix_mult(A, B, C);
return ;
}
#ifdef __cplusplus
extern "C"
#endif
void apatb_matrix_mult_sw(int (*A)[4], int (*B)[4], int (*C)[4]){
apatb_matrix_mult_ir(A, B, C);
return ;
}
#endif
# 29 "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/src/matrix_mult.cpp"

