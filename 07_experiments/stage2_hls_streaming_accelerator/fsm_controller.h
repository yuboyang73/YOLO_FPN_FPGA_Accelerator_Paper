#ifndef FSM_CONTROLLER_H
#define FSM_CONTROLLER_H

enum fsm_state_t {
    FSM_IDLE = 0,
    FSM_FILL_BUFFER = 1,
    FSM_PROCESS = 2
};

void fsm_controller(
    bool reset,
    bool start,
    int row_index,
    int col_index,
    fsm_state_t *state,
    bool *fill_done,
    bool *process_enable);

#endif
