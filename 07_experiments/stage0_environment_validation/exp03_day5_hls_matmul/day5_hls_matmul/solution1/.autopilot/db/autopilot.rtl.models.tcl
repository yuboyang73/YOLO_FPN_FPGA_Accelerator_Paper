set SynModuleInfo {
  {SRCNAME matrix_mult MODELNAME matrix_mult RTLNAME matrix_mult IS_TOP 1
    SUBMODULES {
      {MODELNAME matrix_mult_mul_32s_32s_32_2_1 RTLNAME matrix_mult_mul_32s_32s_32_2_1 BINDTYPE op TYPE mul IMPL auto LATENCY 1 ALLOW_PRAGMA 1}
      {MODELNAME matrix_mult_control_s_axi RTLNAME matrix_mult_control_s_axi BINDTYPE interface TYPE interface_s_axilite}
      {MODELNAME matrix_mult_flow_control_loop_pipe RTLNAME matrix_mult_flow_control_loop_pipe BINDTYPE interface TYPE internal_upc_flow_control INSTNAME matrix_mult_flow_control_loop_pipe_U}
    }
  }
}
