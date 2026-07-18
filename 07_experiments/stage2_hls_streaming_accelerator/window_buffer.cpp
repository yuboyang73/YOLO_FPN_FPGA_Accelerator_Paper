#include "window_buffer.h"

void window_buffer_update(
    const data_t new_column[WINDOW_SIZE],
    data_t window[WINDOW_SIZE][WINDOW_SIZE]) {
#pragma HLS INTERFACE ap_memory port=new_column
#pragma HLS INTERFACE ap_memory port=window
#pragma HLS INLINE off

    for (int row = 0; row < WINDOW_SIZE; ++row) {
        window[row][0] = window[row][1];
        window[row][1] = window[row][2];
        window[row][2] = new_column[row];
    }
}
