# Run C/RTL co-simulation for the AXI4-Stream top function.
cd D:/\.HLS/streaming_frontend_core
open_project streaming_frontend_core
open_solution solution1
source ./streaming_frontend_core/solution1/directives.tcl
cosim_design -rtl verilog -tool xsim -trace_level none
exit
