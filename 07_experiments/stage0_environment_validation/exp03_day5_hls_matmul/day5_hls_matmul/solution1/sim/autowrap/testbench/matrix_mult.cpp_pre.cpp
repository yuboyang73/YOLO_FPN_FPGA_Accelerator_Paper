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
