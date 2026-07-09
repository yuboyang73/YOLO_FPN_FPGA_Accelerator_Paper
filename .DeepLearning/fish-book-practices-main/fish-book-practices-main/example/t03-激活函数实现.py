import matplotlib.pyplot as plt
import numpy as np

# 设置字体为华文细黑
plt.rcParams['font.sans-serif'] = ['STHeiti']  # macOS 上的华文细黑
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

x = np.arange(-10.0, 10.0, 0.1)


def step_function(x):
    return np.array(x > 0, dtype=np.int32)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    return np.maximum(0, x)


y1 = step_function(x)
y2 = sigmoid(x)
y3 = relu(x)

# plt.plot(x, y1, label='(阶跃函数)')
# plt.plot(x, y2, label='(sigmoid函数)')
plt.plot(x, y3, label='(ReLU函数)')
plt.ylim(-0.1, 10.1)
plt.legend()
plt.show()
