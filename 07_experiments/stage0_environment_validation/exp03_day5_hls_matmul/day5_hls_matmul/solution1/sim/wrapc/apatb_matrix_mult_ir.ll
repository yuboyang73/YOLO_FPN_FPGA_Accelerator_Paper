; ModuleID = 'D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage0_environment_validation/exp03_day5_hls_matmul/day5_hls_matmul/solution1/.autopilot/db/a.g.ld.5.gdce.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-i128:128-i256:256-i512:512-i1024:1024-i2048:2048-i4096:4096-n8:16:32:64-S128-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024"
target triple = "fpga64-xilinx-none"

; Function Attrs: inaccessiblemem_or_argmemonly noinline
define void @apatb_matrix_mult_ir([4 x i32]* noalias nocapture nonnull readonly "fpga.decayed.dim.hint"="4" %A, [4 x i32]* noalias nocapture nonnull readonly "fpga.decayed.dim.hint"="4" %B, [4 x i32]* noalias nocapture nonnull "fpga.decayed.dim.hint"="4" %C) local_unnamed_addr #0 {
entry:
  %A_copy = alloca [4 x [4 x i32]], align 512
  %B_copy = alloca [4 x [4 x i32]], align 512
  %C_copy = alloca [4 x [4 x i32]], align 512
  %0 = bitcast [4 x i32]* %A to [4 x [4 x i32]]*
  %1 = bitcast [4 x i32]* %B to [4 x [4 x i32]]*
  %2 = bitcast [4 x i32]* %C to [4 x [4 x i32]]*
  call fastcc void @copy_in([4 x [4 x i32]]* nonnull %0, [4 x [4 x i32]]* nonnull align 512 %A_copy, [4 x [4 x i32]]* nonnull %1, [4 x [4 x i32]]* nonnull align 512 %B_copy, [4 x [4 x i32]]* nonnull %2, [4 x [4 x i32]]* nonnull align 512 %C_copy)
  %3 = getelementptr inbounds [4 x [4 x i32]], [4 x [4 x i32]]* %A_copy, i32 0, i32 0
  %4 = getelementptr inbounds [4 x [4 x i32]], [4 x [4 x i32]]* %B_copy, i32 0, i32 0
  %5 = getelementptr inbounds [4 x [4 x i32]], [4 x [4 x i32]]* %C_copy, i32 0, i32 0
  call void @apatb_matrix_mult_hw([4 x i32]* %3, [4 x i32]* %4, [4 x i32]* %5)
  call void @copy_back([4 x [4 x i32]]* %0, [4 x [4 x i32]]* %A_copy, [4 x [4 x i32]]* %1, [4 x [4 x i32]]* %B_copy, [4 x [4 x i32]]* %2, [4 x [4 x i32]]* %C_copy)
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @copy_in([4 x [4 x i32]]* noalias readonly, [4 x [4 x i32]]* noalias align 512, [4 x [4 x i32]]* noalias readonly, [4 x [4 x i32]]* noalias align 512, [4 x [4 x i32]]* noalias readonly, [4 x [4 x i32]]* noalias align 512) unnamed_addr #1 {
entry:
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* align 512 %1, [4 x [4 x i32]]* %0)
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* align 512 %3, [4 x [4 x i32]]* %2)
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* align 512 %5, [4 x [4 x i32]]* %4)
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* noalias align 512, [4 x [4 x i32]]* noalias readonly) unnamed_addr #2 {
entry:
  %2 = icmp eq [4 x [4 x i32]]* %0, null
  %3 = icmp eq [4 x [4 x i32]]* %1, null
  %4 = or i1 %2, %3
  br i1 %4, label %ret, label %copy

copy:                                             ; preds = %entry
  br label %for.loop

for.loop:                                         ; preds = %for.loop.split, %copy
  %for.loop.idx10 = phi i64 [ 0, %copy ], [ %for.loop.idx.next, %for.loop.split ]
  br label %for.loop2

for.loop2:                                        ; preds = %for.loop2, %for.loop
  %for.loop.idx39 = phi i64 [ 0, %for.loop ], [ %for.loop.idx3.next, %for.loop2 ]
  %dst.addr57 = getelementptr [4 x [4 x i32]], [4 x [4 x i32]]* %0, i64 0, i64 %for.loop.idx10, i64 %for.loop.idx39
  %src.addr68 = getelementptr [4 x [4 x i32]], [4 x [4 x i32]]* %1, i64 0, i64 %for.loop.idx10, i64 %for.loop.idx39
  %5 = load i32, i32* %src.addr68, align 4
  store i32 %5, i32* %dst.addr57, align 4
  %for.loop.idx3.next = add nuw nsw i64 %for.loop.idx39, 1
  %exitcond = icmp ne i64 %for.loop.idx3.next, 4
  br i1 %exitcond, label %for.loop2, label %for.loop.split

for.loop.split:                                   ; preds = %for.loop2
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx10, 1
  %exitcond11 = icmp ne i64 %for.loop.idx.next, 4
  br i1 %exitcond11, label %for.loop, label %ret

ret:                                              ; preds = %for.loop.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @copy_out([4 x [4 x i32]]* noalias, [4 x [4 x i32]]* noalias readonly align 512, [4 x [4 x i32]]* noalias, [4 x [4 x i32]]* noalias readonly align 512, [4 x [4 x i32]]* noalias, [4 x [4 x i32]]* noalias readonly align 512) unnamed_addr #3 {
entry:
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* %0, [4 x [4 x i32]]* align 512 %1)
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* %2, [4 x [4 x i32]]* align 512 %3)
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* %4, [4 x [4 x i32]]* align 512 %5)
  ret void
}

declare void @apatb_matrix_mult_hw([4 x i32]*, [4 x i32]*, [4 x i32]*)

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @copy_back([4 x [4 x i32]]* noalias, [4 x [4 x i32]]* noalias readonly align 512, [4 x [4 x i32]]* noalias, [4 x [4 x i32]]* noalias readonly align 512, [4 x [4 x i32]]* noalias, [4 x [4 x i32]]* noalias readonly align 512) unnamed_addr #3 {
entry:
  call fastcc void @onebyonecpy_hls.p0a4a4i32([4 x [4 x i32]]* %4, [4 x [4 x i32]]* align 512 %5)
  ret void
}

define void @matrix_mult_hw_stub_wrapper([4 x i32]*, [4 x i32]*, [4 x i32]*) #4 {
entry:
  %3 = bitcast [4 x i32]* %0 to [4 x [4 x i32]]*
  %4 = bitcast [4 x i32]* %1 to [4 x [4 x i32]]*
  %5 = bitcast [4 x i32]* %2 to [4 x [4 x i32]]*
  call void @copy_out([4 x [4 x i32]]* null, [4 x [4 x i32]]* %3, [4 x [4 x i32]]* null, [4 x [4 x i32]]* %4, [4 x [4 x i32]]* null, [4 x [4 x i32]]* %5)
  %6 = bitcast [4 x [4 x i32]]* %3 to [4 x i32]*
  %7 = bitcast [4 x [4 x i32]]* %4 to [4 x i32]*
  %8 = bitcast [4 x [4 x i32]]* %5 to [4 x i32]*
  call void @matrix_mult_hw_stub([4 x i32]* %6, [4 x i32]* %7, [4 x i32]* %8)
  call void @copy_in([4 x [4 x i32]]* null, [4 x [4 x i32]]* %3, [4 x [4 x i32]]* null, [4 x [4 x i32]]* %4, [4 x [4 x i32]]* null, [4 x [4 x i32]]* %5)
  ret void
}

declare void @matrix_mult_hw_stub([4 x i32]*, [4 x i32]*, [4 x i32]*)

attributes #0 = { inaccessiblemem_or_argmemonly noinline "fpga.wrapper.func"="wrapper" }
attributes #1 = { argmemonly noinline norecurse "fpga.wrapper.func"="copyin" }
attributes #2 = { argmemonly noinline norecurse "fpga.wrapper.func"="onebyonecpy_hls" }
attributes #3 = { argmemonly noinline norecurse "fpga.wrapper.func"="copyout" }
attributes #4 = { "fpga.wrapper.func"="stub" }

!llvm.dbg.cu = !{}
!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3}
!blackbox_cfg = !{!4}

!0 = !{!"clang version 7.0.0 "}
!1 = !{i32 2, !"Dwarf Version", i32 4}
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 4}
!4 = !{}
