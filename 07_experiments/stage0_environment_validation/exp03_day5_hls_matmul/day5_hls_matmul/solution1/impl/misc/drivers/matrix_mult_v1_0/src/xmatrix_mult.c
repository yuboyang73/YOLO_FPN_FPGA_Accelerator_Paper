// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.2 (64-bit)
// Tool Version Limit: 2019.12
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// ==============================================================
/***************************** Include Files *********************************/
#include "xmatrix_mult.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XMatrix_mult_CfgInitialize(XMatrix_mult *InstancePtr, XMatrix_mult_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XMatrix_mult_Start(XMatrix_mult *InstancePtr) {
    u32 Data;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL) & 0x80;
    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}

u32 XMatrix_mult_IsDone(XMatrix_mult *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL);
    return (Data >> 1) & 0x1;
}

u32 XMatrix_mult_IsIdle(XMatrix_mult *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL);
    return (Data >> 2) & 0x1;
}

u32 XMatrix_mult_IsReady(XMatrix_mult *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL);
    // check ap_start to see if the pcore is ready for next input
    return !(Data & 0x1);
}

void XMatrix_mult_EnableAutoRestart(XMatrix_mult *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL, 0x80);
}

void XMatrix_mult_DisableAutoRestart(XMatrix_mult *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_AP_CTRL, 0);
}

u32 XMatrix_mult_Get_A_BaseAddress(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_A_BASE);
}

u32 XMatrix_mult_Get_A_HighAddress(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_A_HIGH);
}

u32 XMatrix_mult_Get_A_TotalBytes(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XMATRIX_MULT_CONTROL_ADDR_A_HIGH - XMATRIX_MULT_CONTROL_ADDR_A_BASE + 1);
}

u32 XMatrix_mult_Get_A_BitWidth(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMATRIX_MULT_CONTROL_WIDTH_A;
}

u32 XMatrix_mult_Get_A_Depth(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMATRIX_MULT_CONTROL_DEPTH_A;
}

u32 XMatrix_mult_Write_A_Words(XMatrix_mult *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XMATRIX_MULT_CONTROL_ADDR_A_HIGH - XMATRIX_MULT_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_A_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XMatrix_mult_Read_A_Words(XMatrix_mult *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XMATRIX_MULT_CONTROL_ADDR_A_HIGH - XMATRIX_MULT_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_A_BASE + (offset + i)*4);
    }
    return length;
}

u32 XMatrix_mult_Write_A_Bytes(XMatrix_mult *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XMATRIX_MULT_CONTROL_ADDR_A_HIGH - XMATRIX_MULT_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_A_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XMatrix_mult_Read_A_Bytes(XMatrix_mult *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XMATRIX_MULT_CONTROL_ADDR_A_HIGH - XMATRIX_MULT_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_A_BASE + offset + i);
    }
    return length;
}

u32 XMatrix_mult_Get_B_BaseAddress(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_B_BASE);
}

u32 XMatrix_mult_Get_B_HighAddress(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_B_HIGH);
}

u32 XMatrix_mult_Get_B_TotalBytes(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XMATRIX_MULT_CONTROL_ADDR_B_HIGH - XMATRIX_MULT_CONTROL_ADDR_B_BASE + 1);
}

u32 XMatrix_mult_Get_B_BitWidth(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMATRIX_MULT_CONTROL_WIDTH_B;
}

u32 XMatrix_mult_Get_B_Depth(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMATRIX_MULT_CONTROL_DEPTH_B;
}

u32 XMatrix_mult_Write_B_Words(XMatrix_mult *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XMATRIX_MULT_CONTROL_ADDR_B_HIGH - XMATRIX_MULT_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_B_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XMatrix_mult_Read_B_Words(XMatrix_mult *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XMATRIX_MULT_CONTROL_ADDR_B_HIGH - XMATRIX_MULT_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_B_BASE + (offset + i)*4);
    }
    return length;
}

u32 XMatrix_mult_Write_B_Bytes(XMatrix_mult *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XMATRIX_MULT_CONTROL_ADDR_B_HIGH - XMATRIX_MULT_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_B_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XMatrix_mult_Read_B_Bytes(XMatrix_mult *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XMATRIX_MULT_CONTROL_ADDR_B_HIGH - XMATRIX_MULT_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_B_BASE + offset + i);
    }
    return length;
}

u32 XMatrix_mult_Get_C_BaseAddress(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_C_BASE);
}

u32 XMatrix_mult_Get_C_HighAddress(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_C_HIGH);
}

u32 XMatrix_mult_Get_C_TotalBytes(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XMATRIX_MULT_CONTROL_ADDR_C_HIGH - XMATRIX_MULT_CONTROL_ADDR_C_BASE + 1);
}

u32 XMatrix_mult_Get_C_BitWidth(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMATRIX_MULT_CONTROL_WIDTH_C;
}

u32 XMatrix_mult_Get_C_Depth(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMATRIX_MULT_CONTROL_DEPTH_C;
}

u32 XMatrix_mult_Write_C_Words(XMatrix_mult *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XMATRIX_MULT_CONTROL_ADDR_C_HIGH - XMATRIX_MULT_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_C_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XMatrix_mult_Read_C_Words(XMatrix_mult *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XMATRIX_MULT_CONTROL_ADDR_C_HIGH - XMATRIX_MULT_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_C_BASE + (offset + i)*4);
    }
    return length;
}

u32 XMatrix_mult_Write_C_Bytes(XMatrix_mult *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XMATRIX_MULT_CONTROL_ADDR_C_HIGH - XMATRIX_MULT_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_C_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XMatrix_mult_Read_C_Bytes(XMatrix_mult *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XMATRIX_MULT_CONTROL_ADDR_C_HIGH - XMATRIX_MULT_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XMATRIX_MULT_CONTROL_ADDR_C_BASE + offset + i);
    }
    return length;
}

void XMatrix_mult_InterruptGlobalEnable(XMatrix_mult *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_GIE, 1);
}

void XMatrix_mult_InterruptGlobalDisable(XMatrix_mult *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_GIE, 0);
}

void XMatrix_mult_InterruptEnable(XMatrix_mult *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_IER);
    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_IER, Register | Mask);
}

void XMatrix_mult_InterruptDisable(XMatrix_mult *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_IER);
    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_IER, Register & (~Mask));
}

void XMatrix_mult_InterruptClear(XMatrix_mult *InstancePtr, u32 Mask) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XMatrix_mult_WriteReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_ISR, Mask);
}

u32 XMatrix_mult_InterruptGetEnabled(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_IER);
}

u32 XMatrix_mult_InterruptGetStatus(XMatrix_mult *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XMatrix_mult_ReadReg(InstancePtr->Control_BaseAddress, XMATRIX_MULT_CONTROL_ADDR_ISR);
}

