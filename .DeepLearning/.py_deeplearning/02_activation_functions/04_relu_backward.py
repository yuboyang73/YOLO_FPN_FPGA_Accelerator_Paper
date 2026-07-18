"""
ReLU 的反向传播
"""
import numpy as np

#dout：上游传来的梯度 x：ReLU前向传播时的输入
def relu_backward(dout,x):
    dx = dout.copy() #复制一份dout。名为dx
    dx[x <= 0] = 0 #dx的布尔索引，小于0 true，大于0 false
    return dx

def main():
    X = np.array([-2.0,0.0,3.0])
    dout = np.array([10.0,10.0,10.0])

    dX = relu_backward(dout,X)

    print("X.shape =", X.shape)
    print("dout.shape =", dout.shape)
    print("dX.shape =", dX.shape)
    print("X =", X)
    print("dout =", dout)
    print("dX =", dX)


if __name__ == "__main__":
    main()

