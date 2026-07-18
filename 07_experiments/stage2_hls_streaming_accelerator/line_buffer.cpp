#include "line_buffer.h"

void line_buffer_shift_row(
    const data_t input_row[IMAGE_WIDTH],
    data_t line_buf[BUFFER_ROWS][IMAGE_WIDTH],
    data_t old_rows[BUFFER_ROWS][IMAGE_WIDTH]) {
#pragma HLS INTERFACE ap_memory port=input_row
#pragma HLS INTERFACE ap_memory port=line_buf
#pragma HLS INTERFACE ap_memory port=old_rows
#pragma HLS INLINE off

    for (int col = 0; col < IMAGE_WIDTH; ++col) {
        old_rows[0][col] = line_buf[0][col];
        old_rows[1][col] = line_buf[1][col];

        line_buf[0][col] = line_buf[1][col];
        line_buf[1][col] = input_row[col];
    }
}
