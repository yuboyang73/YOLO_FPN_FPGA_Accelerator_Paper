import numpy as np

# X.shape = (2, 3)
# 2 samples, each sample has 3 input features.
X = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

# W.shape = (3, 2)
# 3 input features are mapped to 2 output neurons.
W = np.array([
    [10, 20],
    [30, 40],
    [50, 60]
])

# b.shape = (2,)
# Each output neuron has one bias value.
b = np.array([1, 2])

linear_output = X @ W
Y = linear_output + b

print("X:")
print(X)
print("X.shape:", X.shape)

print("W:")
print(W)
print("W.shape:", W.shape)

print("b:")
print(b)
print("b.shape:", b.shape)

print("X @ W:")
print(linear_output)
print("(X @ W).shape:", linear_output.shape)

print("Y = X @ W + b:")
print(Y)
print("Y.shape:", Y.shape)
