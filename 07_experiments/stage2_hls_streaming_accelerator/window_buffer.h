#ifndef WINDOW_BUFFER_H
#define WINDOW_BUFFER_H

#include <ap_fixed.h>

static const int WINDOW_SIZE = 3;

typedef ap_fixed<16, 8> data_t;

void window_buffer_update(
    const data_t new_column[WINDOW_SIZE],
    data_t window[WINDOW_SIZE][WINDOW_SIZE]);

#endif
