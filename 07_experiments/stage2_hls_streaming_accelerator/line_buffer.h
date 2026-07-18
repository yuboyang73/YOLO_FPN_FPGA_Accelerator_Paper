#ifndef LINE_BUFFER_H
#define LINE_BUFFER_H

#include <ap_fixed.h>

static const int BUFFER_ROWS = 2;
static const int IMAGE_WIDTH = 5;

typedef ap_fixed<16, 8> data_t;

void line_buffer_shift_row(
    const data_t input_row[IMAGE_WIDTH],
    data_t line_buf[BUFFER_ROWS][IMAGE_WIDTH],
    data_t old_rows[BUFFER_ROWS][IMAGE_WIDTH]);

#endif
