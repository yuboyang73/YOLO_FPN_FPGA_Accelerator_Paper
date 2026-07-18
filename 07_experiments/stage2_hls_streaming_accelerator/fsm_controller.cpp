#include "fsm_controller.h"

void fsm_controller(
    bool reset,
    bool start,
    int row_index,
    int col_index,
    fsm_state_t *state,
    bool *fill_done,
    bool *process_enable) {
#pragma HLS INTERFACE ap_none port=reset
#pragma HLS INTERFACE ap_none port=start
#pragma HLS INTERFACE ap_none port=row_index
#pragma HLS INTERFACE ap_none port=col_index
#pragma HLS INTERFACE ap_none port=state
#pragma HLS INTERFACE ap_none port=fill_done
#pragma HLS INTERFACE ap_none port=process_enable
#pragma HLS INLINE off

    *fill_done = false;
    *process_enable = false;

    if (reset || !start) {
        *state = FSM_IDLE;
        return;
    }

    // A 3x3 window requires the first two rows to be filled before
    // processing can start.
    if (row_index < 2) {
        *state = FSM_FILL_BUFFER;
        return;
    }

    *fill_done = true;
    *state = FSM_PROCESS;

    // A 3x3 window becomes valid at row=2, col=2.
    if (row_index >= 2 && col_index >= 2) {
        *process_enable = true;
    }
}
