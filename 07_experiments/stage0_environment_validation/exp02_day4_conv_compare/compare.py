import numpy as np

# =========================
# Load outputs
# =========================
python_output = np.loadtxt("python_output.txt", dtype=np.float64)
cpp_output = np.loadtxt("cpp_output.txt", dtype=np.float64)

# =========================
# Shape check
# =========================
if python_output.shape != cpp_output.shape:
    raise ValueError(
        f"Shape mismatch: "
        f"python_output shape = {python_output.shape}, "
        f"cpp_output shape = {cpp_output.shape}"
    )

# =========================
# Error calculation
# =========================
diff = cpp_output - python_output
mse = np.mean(diff ** 2)
max_abs_error = np.max(np.abs(diff))

# =========================
# Element-wise comparison
# =========================
print("========== Element-wise Comparison ==========")

for i in range(python_output.shape[0]):
    for j in range(python_output.shape[1]):
        print(
            f"[{i}][{j}] "
            f"python={python_output[i, j]: .17g}, "
            f"cpp={cpp_output[i, j]: .17g}, "
            f"diff={diff[i, j]: .17g}"
        )

print("=============================================")
print(f"MSE          = {mse:.17e}")
print(f"MaxAbsError  = {max_abs_error:.17e}")

# =========================
# Pass / Fail check
# =========================
if mse < 1e-15:
    print("PASS: C++ output matches Python reference. MSE < 1e-15")
else:
    print("FAIL: C++ output does not match Python reference. MSE >= 1e-15")