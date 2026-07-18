"""
单个样本经过 Affine 层
"""
import numpy as np

#x = [身高标准化值, 体重标准化值, 年龄标准化值]
X = np.array([1,2,3])
#(3,2)3个输入特征数，2两个输出神经元
W = np.array([
    [10,20],
    [30,40],
    [50,60]
])
b = np.array([1,2])

Y = X @ W + b
print(Y)