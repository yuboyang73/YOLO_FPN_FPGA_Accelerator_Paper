; ModuleID = 'D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/stage2_hls_streaming_accelerator/conv3x3_core/conv3x3_core/solution1/.autopilot/db/a.g.ld.5.gdce.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-i128:128-i256:256-i512:512-i1024:1024-i2048:2048-i4096:4096-n8:16:32:64-S128-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024"
target triple = "fpga64-xilinx-none"

%"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>" = type { %"struct.ap_fixed_base<16, 8, true, AP_TRN, AP_WRAP, 0>" }
%"struct.ap_fixed_base<16, 8, true, AP_TRN, AP_WRAP, 0>" = type { %"struct.ssdm_int<16, true>" }
%"struct.ssdm_int<16, true>" = type { i16 }

; Function Attrs: noinline
define void @apatb_conv3x3_core_ir([40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]* noalias nocapture nonnull readonly "fpga.decayed.dim.hint"="64" %input, [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias nocapture nonnull readonly "fpga.decayed.dim.hint"="64" %weights, [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]* noalias nocapture nonnull "fpga.decayed.dim.hint"="64" %output) local_unnamed_addr #0 {
entry:
  %malloccall = call i8* @malloc(i64 204800)
  %input_copy = bitcast i8* %malloccall to [64 x [40 x [40 x i16]]]*
  %malloccall1 = call i8* @malloc(i64 73728)
  %weights_copy = bitcast i8* %malloccall1 to [64 x [64 x [3 x [3 x i16]]]]*
  %malloccall2 = call i8* @malloc(i64 204800)
  %output_copy = bitcast i8* %malloccall2 to [64 x [40 x [40 x i16]]]*
  %0 = bitcast [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]* %input to [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]*
  %1 = bitcast [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %weights to [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]*
  %2 = bitcast [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]* %output to [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]*
  call fastcc void @copy_in([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* nonnull %0, [64 x [40 x [40 x i16]]]* %input_copy, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* nonnull %1, [64 x [64 x [3 x [3 x i16]]]]* %weights_copy, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* nonnull %2, [64 x [40 x [40 x i16]]]* %output_copy)
  %3 = getelementptr [64 x [40 x [40 x i16]]], [64 x [40 x [40 x i16]]]* %input_copy, i32 0, i32 0
  %4 = getelementptr [64 x [64 x [3 x [3 x i16]]]], [64 x [64 x [3 x [3 x i16]]]]* %weights_copy, i32 0, i32 0
  %5 = getelementptr [64 x [40 x [40 x i16]]], [64 x [40 x [40 x i16]]]* %output_copy, i32 0, i32 0
  call void @apatb_conv3x3_core_hw([40 x [40 x i16]]* %3, [64 x [3 x [3 x i16]]]* %4, [40 x [40 x i16]]* %5)
  call void @copy_back([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %0, [64 x [40 x [40 x i16]]]* %input_copy, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %1, [64 x [64 x [3 x [3 x i16]]]]* %weights_copy, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %2, [64 x [40 x [40 x i16]]]* %output_copy)
  call void @free(i8* %malloccall)
  call void @free(i8* %malloccall1)
  call void @free(i8* %malloccall2)
  ret void
}

declare noalias i8* @malloc(i64) local_unnamed_addr

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @copy_in([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias readonly, [64 x [40 x [40 x i16]]]* noalias, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* noalias readonly, [64 x [64 x [3 x [3 x i16]]]]* noalias, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias readonly, [64 x [40 x [40 x i16]]]* noalias) unnamed_addr #1 {
entry:
  call fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"([64 x [40 x [40 x i16]]]* %1, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %0)
  call fastcc void @"onebyonecpy_hls.p0a64a64a3a3struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>.300"([64 x [64 x [3 x [3 x i16]]]]* %3, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %2)
  call fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"([64 x [40 x [40 x i16]]]* %5, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %4)
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @"onebyonecpy_hls.p0a64a64a3a3struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"([64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* noalias, [64 x [64 x [3 x [3 x i16]]]]* noalias readonly) unnamed_addr #2 {
entry:
  %2 = icmp eq [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %0, null
  %3 = icmp eq [64 x [64 x [3 x [3 x i16]]]]* %1, null
  %4 = or i1 %2, %3
  br i1 %4, label %ret, label %copy

copy:                                             ; preds = %entry
  br label %for.loop

for.loop:                                         ; preds = %for.loop.split, %copy
  %for.loop.idx34 = phi i64 [ 0, %copy ], [ %for.loop.idx.next, %for.loop.split ]
  br label %for.loop2

for.loop2:                                        ; preds = %for.loop2.split, %for.loop
  %for.loop.idx333 = phi i64 [ 0, %for.loop ], [ %for.loop.idx3.next, %for.loop2.split ]
  br label %for.loop8

for.loop8:                                        ; preds = %for.loop8.split, %for.loop2
  %for.loop.idx932 = phi i64 [ 0, %for.loop2 ], [ %for.loop.idx9.next, %for.loop8.split ]
  br label %for.loop14

for.loop14:                                       ; preds = %for.loop14, %for.loop8
  %for.loop.idx1531 = phi i64 [ 0, %for.loop8 ], [ %for.loop.idx15.next, %for.loop14 ]
  %5 = getelementptr [64 x [64 x [3 x [3 x i16]]]], [64 x [64 x [3 x [3 x i16]]]]* %1, i64 0, i64 %for.loop.idx34, i64 %for.loop.idx333, i64 %for.loop.idx932, i64 %for.loop.idx1531
  %dst.addr17.0.0.030 = getelementptr [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]], [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %0, i64 0, i64 %for.loop.idx34, i64 %for.loop.idx333, i64 %for.loop.idx932, i64 %for.loop.idx1531, i32 0, i32 0, i32 0
  %6 = load i16, i16* %5, align 2
  store i16 %6, i16* %dst.addr17.0.0.030, align 2
  %for.loop.idx15.next = add nuw nsw i64 %for.loop.idx1531, 1
  %exitcond = icmp ne i64 %for.loop.idx15.next, 3
  br i1 %exitcond, label %for.loop14, label %for.loop8.split

for.loop8.split:                                  ; preds = %for.loop14
  %for.loop.idx9.next = add nuw nsw i64 %for.loop.idx932, 1
  %exitcond35 = icmp ne i64 %for.loop.idx9.next, 3
  br i1 %exitcond35, label %for.loop8, label %for.loop2.split

for.loop2.split:                                  ; preds = %for.loop8.split
  %for.loop.idx3.next = add nuw nsw i64 %for.loop.idx333, 1
  %exitcond36 = icmp ne i64 %for.loop.idx3.next, 64
  br i1 %exitcond36, label %for.loop2, label %for.loop.split

for.loop.split:                                   ; preds = %for.loop2.split
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx34, 1
  %exitcond37 = icmp ne i64 %for.loop.idx.next, 64
  br i1 %exitcond37, label %for.loop, label %ret

ret:                                              ; preds = %for.loop.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @copy_out([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias, [64 x [40 x [40 x i16]]]* noalias readonly, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* noalias, [64 x [64 x [3 x [3 x i16]]]]* noalias readonly, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias, [64 x [40 x [40 x i16]]]* noalias readonly) unnamed_addr #3 {
entry:
  call fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>.292"([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %0, [64 x [40 x [40 x i16]]]* %1)
  call fastcc void @"onebyonecpy_hls.p0a64a64a3a3struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"([64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %2, [64 x [64 x [3 x [3 x i16]]]]* %3)
  call fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>.292"([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %4, [64 x [40 x [40 x i16]]]* %5)
  ret void
}

declare void @free(i8*) local_unnamed_addr

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>.292"([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias, [64 x [40 x [40 x i16]]]* noalias readonly) unnamed_addr #2 {
entry:
  %2 = icmp eq [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %0, null
  %3 = icmp eq [64 x [40 x [40 x i16]]]* %1, null
  %4 = or i1 %2, %3
  br i1 %4, label %ret, label %copy

copy:                                             ; preds = %entry
  br label %for.loop

for.loop:                                         ; preds = %for.loop.split, %copy
  %for.loop.idx25 = phi i64 [ 0, %copy ], [ %for.loop.idx.next, %for.loop.split ]
  br label %for.loop2

for.loop2:                                        ; preds = %for.loop2.split, %for.loop
  %for.loop.idx324 = phi i64 [ 0, %for.loop ], [ %for.loop.idx3.next, %for.loop2.split ]
  br label %for.loop8

for.loop8:                                        ; preds = %for.loop8, %for.loop2
  %for.loop.idx923 = phi i64 [ 0, %for.loop2 ], [ %for.loop.idx9.next, %for.loop8 ]
  %5 = getelementptr [64 x [40 x [40 x i16]]], [64 x [40 x [40 x i16]]]* %1, i64 0, i64 %for.loop.idx25, i64 %for.loop.idx324, i64 %for.loop.idx923
  %dst.addr11.0.0.022 = getelementptr [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]], [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %0, i64 0, i64 %for.loop.idx25, i64 %for.loop.idx324, i64 %for.loop.idx923, i32 0, i32 0, i32 0
  %6 = load i16, i16* %5, align 2
  store i16 %6, i16* %dst.addr11.0.0.022, align 2
  %for.loop.idx9.next = add nuw nsw i64 %for.loop.idx923, 1
  %exitcond = icmp ne i64 %for.loop.idx9.next, 40
  br i1 %exitcond, label %for.loop8, label %for.loop2.split

for.loop2.split:                                  ; preds = %for.loop8
  %for.loop.idx3.next = add nuw nsw i64 %for.loop.idx324, 1
  %exitcond26 = icmp ne i64 %for.loop.idx3.next, 40
  br i1 %exitcond26, label %for.loop2, label %for.loop.split

for.loop.split:                                   ; preds = %for.loop2.split
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx25, 1
  %exitcond27 = icmp ne i64 %for.loop.idx.next, 64
  br i1 %exitcond27, label %for.loop, label %ret

ret:                                              ; preds = %for.loop.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"([64 x [40 x [40 x i16]]]* noalias, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias readonly) unnamed_addr #2 {
entry:
  %2 = icmp eq [64 x [40 x [40 x i16]]]* %0, null
  %3 = icmp eq [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %1, null
  %4 = or i1 %2, %3
  br i1 %4, label %ret, label %copy

copy:                                             ; preds = %entry
  br label %for.loop

for.loop:                                         ; preds = %for.loop.split, %copy
  %for.loop.idx25 = phi i64 [ 0, %copy ], [ %for.loop.idx.next, %for.loop.split ]
  br label %for.loop2

for.loop2:                                        ; preds = %for.loop2.split, %for.loop
  %for.loop.idx324 = phi i64 [ 0, %for.loop ], [ %for.loop.idx3.next, %for.loop2.split ]
  br label %for.loop8

for.loop8:                                        ; preds = %for.loop8, %for.loop2
  %for.loop.idx923 = phi i64 [ 0, %for.loop2 ], [ %for.loop.idx9.next, %for.loop8 ]
  %src.addr12.0.0.021 = getelementptr [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]], [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %1, i64 0, i64 %for.loop.idx25, i64 %for.loop.idx324, i64 %for.loop.idx923, i32 0, i32 0, i32 0
  %5 = getelementptr [64 x [40 x [40 x i16]]], [64 x [40 x [40 x i16]]]* %0, i64 0, i64 %for.loop.idx25, i64 %for.loop.idx324, i64 %for.loop.idx923
  %6 = load i16, i16* %src.addr12.0.0.021, align 2
  store i16 %6, i16* %5, align 2
  %for.loop.idx9.next = add nuw nsw i64 %for.loop.idx923, 1
  %exitcond = icmp ne i64 %for.loop.idx9.next, 40
  br i1 %exitcond, label %for.loop8, label %for.loop2.split

for.loop2.split:                                  ; preds = %for.loop8
  %for.loop.idx3.next = add nuw nsw i64 %for.loop.idx324, 1
  %exitcond26 = icmp ne i64 %for.loop.idx3.next, 40
  br i1 %exitcond26, label %for.loop2, label %for.loop.split

for.loop.split:                                   ; preds = %for.loop2.split
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx25, 1
  %exitcond27 = icmp ne i64 %for.loop.idx.next, 64
  br i1 %exitcond27, label %for.loop, label %ret

ret:                                              ; preds = %for.loop.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @"onebyonecpy_hls.p0a64a64a3a3struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>.300"([64 x [64 x [3 x [3 x i16]]]]* noalias, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* noalias readonly) unnamed_addr #2 {
entry:
  %2 = icmp eq [64 x [64 x [3 x [3 x i16]]]]* %0, null
  %3 = icmp eq [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %1, null
  %4 = or i1 %2, %3
  br i1 %4, label %ret, label %copy

copy:                                             ; preds = %entry
  br label %for.loop

for.loop:                                         ; preds = %for.loop.split, %copy
  %for.loop.idx34 = phi i64 [ 0, %copy ], [ %for.loop.idx.next, %for.loop.split ]
  br label %for.loop2

for.loop2:                                        ; preds = %for.loop2.split, %for.loop
  %for.loop.idx333 = phi i64 [ 0, %for.loop ], [ %for.loop.idx3.next, %for.loop2.split ]
  br label %for.loop8

for.loop8:                                        ; preds = %for.loop8.split, %for.loop2
  %for.loop.idx932 = phi i64 [ 0, %for.loop2 ], [ %for.loop.idx9.next, %for.loop8.split ]
  br label %for.loop14

for.loop14:                                       ; preds = %for.loop14, %for.loop8
  %for.loop.idx1531 = phi i64 [ 0, %for.loop8 ], [ %for.loop.idx15.next, %for.loop14 ]
  %src.addr18.0.0.029 = getelementptr [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]], [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %1, i64 0, i64 %for.loop.idx34, i64 %for.loop.idx333, i64 %for.loop.idx932, i64 %for.loop.idx1531, i32 0, i32 0, i32 0
  %5 = getelementptr [64 x [64 x [3 x [3 x i16]]]], [64 x [64 x [3 x [3 x i16]]]]* %0, i64 0, i64 %for.loop.idx34, i64 %for.loop.idx333, i64 %for.loop.idx932, i64 %for.loop.idx1531
  %6 = load i16, i16* %src.addr18.0.0.029, align 2
  store i16 %6, i16* %5, align 2
  %for.loop.idx15.next = add nuw nsw i64 %for.loop.idx1531, 1
  %exitcond = icmp ne i64 %for.loop.idx15.next, 3
  br i1 %exitcond, label %for.loop14, label %for.loop8.split

for.loop8.split:                                  ; preds = %for.loop14
  %for.loop.idx9.next = add nuw nsw i64 %for.loop.idx932, 1
  %exitcond35 = icmp ne i64 %for.loop.idx9.next, 3
  br i1 %exitcond35, label %for.loop8, label %for.loop2.split

for.loop2.split:                                  ; preds = %for.loop8.split
  %for.loop.idx3.next = add nuw nsw i64 %for.loop.idx333, 1
  %exitcond36 = icmp ne i64 %for.loop.idx3.next, 64
  br i1 %exitcond36, label %for.loop2, label %for.loop.split

for.loop.split:                                   ; preds = %for.loop2.split
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx34, 1
  %exitcond37 = icmp ne i64 %for.loop.idx.next, 64
  br i1 %exitcond37, label %for.loop, label %ret

ret:                                              ; preds = %for.loop.split, %entry
  ret void
}

declare void @apatb_conv3x3_core_hw([40 x [40 x i16]]*, [64 x [3 x [3 x i16]]]*, [40 x [40 x i16]]*)

; Function Attrs: argmemonly noinline norecurse
define internal fastcc void @copy_back([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias, [64 x [40 x [40 x i16]]]* noalias readonly, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* noalias, [64 x [64 x [3 x [3 x i16]]]]* noalias readonly, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* noalias, [64 x [40 x [40 x i16]]]* noalias readonly) unnamed_addr #3 {
entry:
  call fastcc void @"onebyonecpy_hls.p0a64a40a40struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>.292"([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %4, [64 x [40 x [40 x i16]]]* %5)
  ret void
}

define void @conv3x3_core_hw_stub_wrapper([40 x [40 x i16]]*, [64 x [3 x [3 x i16]]]*, [40 x [40 x i16]]*) #4 {
entry:
  %malloccall = tail call i8* @malloc(i64 204800)
  %3 = bitcast i8* %malloccall to [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]*
  %malloccall1 = tail call i8* @malloc(i64 73728)
  %4 = bitcast i8* %malloccall1 to [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]*
  %malloccall2 = tail call i8* @malloc(i64 204800)
  %5 = bitcast i8* %malloccall2 to [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]*
  %6 = bitcast [40 x [40 x i16]]* %0 to [64 x [40 x [40 x i16]]]*
  %7 = bitcast [64 x [3 x [3 x i16]]]* %1 to [64 x [64 x [3 x [3 x i16]]]]*
  %8 = bitcast [40 x [40 x i16]]* %2 to [64 x [40 x [40 x i16]]]*
  call void @copy_out([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %3, [64 x [40 x [40 x i16]]]* %6, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %4, [64 x [64 x [3 x [3 x i16]]]]* %7, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %5, [64 x [40 x [40 x i16]]]* %8)
  %9 = bitcast [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %3 to [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]*
  %10 = bitcast [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %4 to [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]*
  %11 = bitcast [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %5 to [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]*
  call void @conv3x3_core_hw_stub([40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]* %9, [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %10, [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]* %11)
  call void @copy_in([64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %3, [64 x [40 x [40 x i16]]]* %6, [64 x [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]]* %4, [64 x [64 x [3 x [3 x i16]]]]* %7, [64 x [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]* %5, [64 x [40 x [40 x i16]]]* %8)
  ret void
}

declare void @conv3x3_core_hw_stub([40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]*, [64 x [3 x [3 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]]*, [40 x [40 x %"struct.ap_fixed<16, 8, AP_TRN, AP_WRAP, 0>"]]*)

attributes #0 = { noinline "fpga.wrapper.func"="wrapper" }
attributes #1 = { argmemonly noinline norecurse "fpga.wrapper.func"="copyin" }
attributes #2 = { argmemonly noinline norecurse "fpga.wrapper.func"="onebyonecpy_hls" }
attributes #3 = { argmemonly noinline norecurse "fpga.wrapper.func"="copyout" }
attributes #4 = { "fpga.wrapper.func"="stub" }

!llvm.dbg.cu = !{}
!llvm.ident = !{!0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3}
!blackbox_cfg = !{!4}

!0 = !{!"clang version 7.0.0 "}
!1 = !{i32 2, !"Dwarf Version", i32 4}
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 4}
!4 = !{}
