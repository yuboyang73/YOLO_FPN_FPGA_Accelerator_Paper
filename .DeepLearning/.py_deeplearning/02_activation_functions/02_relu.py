"""
只保留正响应，把负响应截断为 0
"""
import numpy as np

def ReLU(x):
    return np.maximum(0,x)

def main():
    X = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])

    Y = ReLU(X)

    print("X.shape =", X.shape)
    print("Y.shape =", Y.shape)
    print("X =", X)
    print("Y =", Y)


if __name__ == "__main__":
    main()