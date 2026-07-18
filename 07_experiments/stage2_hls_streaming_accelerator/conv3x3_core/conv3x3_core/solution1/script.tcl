############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
############################################################
open_project conv3x3_core
set_top streaming_frontend
add_files ../conv3x3_core.cpp
add_files ../conv3x3_core.h
add_files ../fsm_controller.cpp
add_files ../fsm_controller.h
add_files ../line_buffer.cpp
add_files ../line_buffer.h
add_files ../streaming_frontend.cpp
add_files ../streaming_frontend.h
add_files ../window_buffer.cpp
add_files ../window_buffer.h
add_files -tb ../tb_streaming_frontend.cpp
open_solution "solution1" -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 5ns -name default
source "./conv3x3_core/solution1/directives.tcl"
csim_design -clean
csynth_design
cosim_design
export_design -format ip_catalog
