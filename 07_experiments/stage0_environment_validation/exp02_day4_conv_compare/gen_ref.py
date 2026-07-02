import numpy as np

# =========================
# Basic configuration
# =========================
H = 5
W = 5
K = 3
STRIDE = 1
PADDING = 0

OH = (H + 2 * PADDING - K) // STRIDE + 1
OW = (W + 2 * PADDING - K) // STRIDE + 1

# =========================
# Input feature map: 5x5
# =========================
x = np.array([
    [1.0,  2.0,  3.0,  4.0,  5.0],
    [6.0,  7.0,  8.0,  9.0, 10.0],
    [11.0, 12.0, 13.0, 14.0, 15.0],
    [16.0, 17.0, 18.0, 19.0, 20.0],
    [21.0, 22.0, 23.0, 24.0, 25.0],
], dtype=np.float64)

# =========================
# 3x3 convolution kernel
# =========================
w = np.array([
    [1.0, 0.0, -1.0],
    [1.0, 0.0, -1.0],
    [1.0, 0.0, -1.0],
], dtype=np.float64)

bias = np.float64(0.0)

# =========================
# Optional padding
# =========================
if PADDING > 0:
    x_pad = np.pad(
        x,
        pad_width=((PADDING, PADDING), (PADDING, PADDING)),
        mode="constant",
        constant_values=0.0
    )
else:
    x_pad = x

# =========================
# Python reference convolution
# =========================
y = np.zeros((OH, OW), dtype=np.float64)

for oh in range(OH):
    for ow in range(OW):
        acc = bias
        for kh in range(K):
            for kw in range(K):
                ih = oh * STRIDE + kh
                iw = ow * STRIDE + kw
                acc += x_pad[ih, iw] * w[kh, kw]
        y[oh, ow] = acc

# =========================
# Save files
# =========================
np.savetxt("input.txt", x, fmt="%.17g")
np.savetxt("weight.txt", w, fmt="%.17g")
np.savetxt("bias.txt", np.array([bias]), fmt="%.17g")
np.savetxt("python_output.txt", y, fmt="%.17g")

# =========================
# Print reference output
# =========================
print("========== Python Reference Output ==========")
print(f"Input shape  : {x.shape}")
print(f"Weight shape : {w.shape}")
print(f"Output shape : {y.shape}")
print()

for i in range(OH):
    for j in range(OW):
        print(f"python_output[{i}][{j}] = {y[i, j]:.17g}")

print("=============================================")
print("Files generated:")
print("  input.txt")
print("  weight.txt")
print("  bias.txt")
print("  python_output.txt")