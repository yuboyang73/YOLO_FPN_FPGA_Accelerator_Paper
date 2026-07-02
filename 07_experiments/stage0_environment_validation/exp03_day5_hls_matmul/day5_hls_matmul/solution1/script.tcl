############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
############################################################
open_project day5_hls_matmul
set_top matrix_mult
add_files src/matrix_mult.cpp
add_files src/matrix_mult.h
add_files -tb tb/matrix_mult_test.cpp
open_solution "solution1" -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10ns -name default
#source "./day5_hls_matmul/solution1/directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
