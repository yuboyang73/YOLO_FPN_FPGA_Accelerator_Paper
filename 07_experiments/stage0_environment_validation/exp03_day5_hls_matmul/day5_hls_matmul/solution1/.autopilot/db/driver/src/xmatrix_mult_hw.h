// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.2 (64-bit)
// Tool Version Limit: 2019.12
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// ==============================================================
// control
// 0x00 : Control signals
//        bit 0  - ap_start (Read/Write/COH)
//        bit 1  - ap_done (Read/COR)
//        bit 2  - ap_idle (Read)
//        bit 3  - ap_ready (Read/COR)
//        bit 7  - auto_restart (Read/Write)
//        bit 9  - interrupt (Read)
//        others - reserved
// 0x04 : Global Interrupt Enable Register
//        bit 0  - Global Interrupt Enable (Read/Write)
//        others - reserved
// 0x08 : IP Interrupt Enable Register (Read/Write)
//        bit 0 - enable ap_done interrupt (Read/Write)
//        bit 1 - enable ap_ready interrupt (Read/Write)
//        others - reserved
// 0x0c : IP Interrupt Status Register (Read/TOW)
//        bit 0 - ap_done (Read/TOW)
//        bit 1 - ap_ready (Read/TOW)
//        others - reserved
// 0x40 ~
// 0x7f : Memory 'A' (16 * 32b)
//        Word n : bit [31:0] - A[n]
// 0x80 ~
// 0xbf : Memory 'B' (16 * 32b)
//        Word n : bit [31:0] - B[n]
// 0xc0 ~
// 0xff : Memory 'C' (16 * 32b)
//        Word n : bit [31:0] - C[n]
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XMATRIX_MULT_CONTROL_ADDR_AP_CTRL 0x00
#define XMATRIX_MULT_CONTROL_ADDR_GIE     0x04
#define XMATRIX_MULT_CONTROL_ADDR_IER     0x08
#define XMATRIX_MULT_CONTROL_ADDR_ISR     0x0c
#define XMATRIX_MULT_CONTROL_ADDR_A_BASE  0x40
#define XMATRIX_MULT_CONTROL_ADDR_A_HIGH  0x7f
#define XMATRIX_MULT_CONTROL_WIDTH_A      32
#define XMATRIX_MULT_CONTROL_DEPTH_A      16
#define XMATRIX_MULT_CONTROL_ADDR_B_BASE  0x80
#define XMATRIX_MULT_CONTROL_ADDR_B_HIGH  0xbf
#define XMATRIX_MULT_CONTROL_WIDTH_B      32
#define XMATRIX_MULT_CONTROL_DEPTH_B      16
#define XMATRIX_MULT_CONTROL_ADDR_C_BASE  0xc0
#define XMATRIX_MULT_CONTROL_ADDR_C_HIGH  0xff
#define XMATRIX_MULT_CONTROL_WIDTH_C      32
#define XMATRIX_MULT_CONTROL_DEPTH_C      16

