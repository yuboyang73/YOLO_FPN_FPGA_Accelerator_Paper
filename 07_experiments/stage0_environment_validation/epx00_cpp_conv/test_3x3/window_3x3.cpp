#include <iostream>
using namespace std;

typedef int data_t;

void shift_window_3x3(data_t window[3][3], data_t new_col[3]) {
    // 1. 每一行左移
    for (int r = 0; r < 3; r++) {
        window[r][0] = window[r][1];
        window[r][1] = window[r][2];
        window[r][2] = new_col[r];
    }
}

void print_window(data_t window[3][3]) {
    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) {
            cout << window[r][c] << " ";
        }
        cout << endl;
    }
    cout << "--------" << endl;
}

int main() {
    data_t window[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    data_t new_col[3] = {10, 11, 12};

    cout << "Before shift:" << endl;
    print_window(window);

    shift_window_3x3(window, new_col);

    cout << "After shift:" << endl;
    print_window(window);

    return 0;
}