# Rebuild the short-path streaming_frontend_core project after source updates.
cd D:/\.HLS/streaming_frontend_core
open_project streaming_frontend_core
open_solution solution1
source ./streaming_frontend_core/solution1/directives.tcl
csim_design -clean
csynth_design
exit
