#include "line_buffer.h"

#include <cmath>
#include <iostream>

int main() {
    data_t line_buf[BUFFER_ROWS][IMAGE_WIDTH];
    data_t old_rows[BUFFER_ROWS][IMAGE_WIDTH];
    data_t input_row[IMAGE_WIDTH];

    for (int row = 0; row < BUFFER_ROWS; ++row) {
        for (int col = 0; col < IMAGE_WIDTH; ++col) {
            line_buf[row][col] = -1;
        }
    }

    bool all_pass = true;

    for (int row = 0; row < 5; ++row) {
        for (int col = 0; col < IMAGE_WIDTH; ++col) {
            input_row[col] = static_cast<data_t>(
                row * IMAGE_WIDTH + col);
        }

        line_buffer_shift_row(input_row, line_buf, old_rows);

        bool row_pass = true;
        for (int col = 0; col < IMAGE_WIDTH; ++col) {
            double expected_row0 = -1.0;
            double expected_row1 = -1.0;

            if (row >= 1) {
                expected_row1 = (row - 1) * IMAGE_WIDTH + col;
            }
            if (row >= 2) {
                expected_row0 = (row - 2) * IMAGE_WIDTH + col;
            }

            const double actual_row0 = old_rows[0][col].to_double();
            const double actual_row1 = old_rows[1][col].to_double();

            if (std::fabs(actual_row0 - expected_row0) > 1e-6 ||
                std::fabs(actual_row1 - expected_row1) > 1e-6) {
                row_pass = false;
                all_pass = false;
            }
        }

        std::cout << "Row " << row << " shift: "
                  << (row_pass ? "PASS" : "FAIL") << std::endl;
    }

    if (all_pass) {
        std::cout << "[PASS] Line Buffer row shifting verified."
                  << std::endl;
        return 0;
    }

    std::cout << "[FAIL] Line Buffer verification failed."
              << std::endl;
    return 1;
}
