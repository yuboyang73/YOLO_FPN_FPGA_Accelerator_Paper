#include "window_buffer.h"

#include <cmath>
#include <iostream>

int main() {
    data_t window[WINDOW_SIZE][WINDOW_SIZE];
    data_t new_column[WINDOW_SIZE];

    const int reference[WINDOW_SIZE][5] = {
        {0, 1, 2, 3, 4},
        {5, 6, 7, 8, 9},
        {10, 11, 12, 13, 14}
    };

    for (int row = 0; row < WINDOW_SIZE; ++row) {
        for (int col = 0; col < WINDOW_SIZE; ++col) {
            window[row][col] = -1;
        }
    }

    bool all_pass = true;

    for (int col = 0; col < 5; ++col) {
        for (int row = 0; row < WINDOW_SIZE; ++row) {
            new_column[row] = static_cast<data_t>(reference[row][col]);
        }

        window_buffer_update(new_column, window);

        bool column_pass = true;
        if (col >= WINDOW_SIZE - 1) {
            const int first_col = col - WINDOW_SIZE + 1;

            for (int row = 0; row < WINDOW_SIZE; ++row) {
                for (int win_col = 0; win_col < WINDOW_SIZE; ++win_col) {
                    const double expected =
                        reference[row][first_col + win_col];
                    const double actual = window[row][win_col].to_double();

                    if (std::fabs(actual - expected) > 1e-6) {
                        column_pass = false;
                        all_pass = false;
                    }
                }
            }
        }

        if (col >= WINDOW_SIZE - 1) {
            std::cout << "Window ending at column " << col << ": "
                      << (column_pass ? "PASS" : "FAIL") << std::endl;
        }
    }

    if (all_pass) {
        std::cout << "[PASS] Window Buffer sliding verified."
                  << std::endl;
        return 0;
    }

    std::cout << "[FAIL] Window Buffer verification failed."
              << std::endl;
    return 1;
}
