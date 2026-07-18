#include "fsm_controller.h"

#include <iostream>

static const char *state_name(fsm_state_t state) {
    switch (state) {
    case FSM_IDLE:
        return "IDLE";
    case FSM_FILL_BUFFER:
        return "FILL_BUFFER";
    case FSM_PROCESS:
        return "PROCESS";
    default:
        return "UNKNOWN";
    }
}

int main() {
    fsm_state_t state = FSM_IDLE;
    bool fill_done = false;
    bool process_enable = false;
    bool all_pass = true;

    fsm_controller(true, false, 0, 0,
                   &state, &fill_done, &process_enable);
    if (state != FSM_IDLE || fill_done || process_enable) {
        all_pass = false;
    }
    std::cout << "Reset state: " << state_name(state) << std::endl;

    for (int row = 0; row < 5; ++row) {
        for (int col = 0; col < 5; ++col) {
            fsm_controller(false, true, row, col,
                           &state, &fill_done, &process_enable);

            const fsm_state_t expected_state =
                (row < 2) ? FSM_FILL_BUFFER : FSM_PROCESS;
            const bool expected_fill_done = row >= 2;
            const bool expected_process_enable = row >= 2 && col >= 2;

            if (state != expected_state ||
                fill_done != expected_fill_done ||
                process_enable != expected_process_enable) {
                all_pass = false;
                std::cout << "Mismatch at row=" << row
                          << ", col=" << col << std::endl;
            }
        }
    }

    if (all_pass) {
        std::cout << "IDLE -> FILL_BUFFER -> PROCESS: PASS" << std::endl;
        std::cout << "First PROCESS enable: row=2, col=2" << std::endl;
        std::cout << "[PASS] FSM controller verified." << std::endl;
        return 0;
    }

    std::cout << "[FAIL] FSM controller verification failed." << std::endl;
    return 1;
}
