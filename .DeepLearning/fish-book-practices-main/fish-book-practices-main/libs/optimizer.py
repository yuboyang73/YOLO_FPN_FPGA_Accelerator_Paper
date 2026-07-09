import abc
from typing import Dict, Any
import numpy as np


class Optimizer(abc.ABC):
    """
    基础优化器类
    """

    @abc.abstractmethod
    def update(self, params: Dict[str, np.array], grads: Dict[str, np.array]) -> None:
        """
        更新参数
        """
        pass


class SGD(Optimizer):
    """
    随机梯度下降优化器
    """

    def __init__(self, lr: float = 0.01):
        """
        初始化优化器
        Args:
            lr (float): 学习率
        """
        self.lr = lr

    def update(self, params: Dict[str, np.array], grads: Dict[str, np.array]):
        """
        更新参数
        Args:
            params (dict): 模型参数
            grads (dict): 梯度
        """
        for key in params.keys():
            params[key] -= self.lr * grads[key]


class Momentum(Optimizer):
    """
    动量优化器
    """

    def __init__(self, lr: float = 0.01, momentum: float = 0.9):
        """
        初始化优化器
        Args:
            lr (float): 学习率
            momentum (float): 动量系数
        """
        self.lr = lr
        self.momentum = momentum
        self.velocity = {}

    def update(self, params: Dict[str, np.array], grads: Dict[str, np.array]):
        """
        更新参数
        Args:
            params (dict): 模型参数
            grads (dict): 梯度
        """
        for key in params.keys():
            if key not in self.velocity:
                self.velocity[key] = np.zeros_like(params[key])
            self.velocity[key] = self.momentum * self.velocity[key] - self.lr * grads[key]
            params[key] += self.velocity[key]


class AdaGrad(Optimizer):
    """
    AdaGrad优化器
    """

    def __init__(self, lr: float = 0.01):
        """
        初始化优化器
        Args:
            lr (float): 学习率
        """
        self.lr = lr
        self.epsilon: float = 1e-8
        self.cache = {}

    def update(self, params: Dict[str, np.array], grads: Dict[str, np.array]):
        """
        更新参数
        Args:
            params (dict): 模型参数
            grads (dict): 梯度
        """
        for key in params.keys():
            if key not in self.cache:
                self.cache[key] = np.zeros_like(params[key])
            self.cache[key] += grads[key] ** 2
            params[key] -= self.lr * grads[key] / (np.sqrt(self.cache[key]) + self.epsilon)


class Adam(Optimizer):
    """
    Adam优化器
    """

    def __init__(self, lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999):
        """
        初始化优化器
        Args:
            lr (float): 学习率
            beta1 (float): 一阶矩估计的衰减率
            beta2 (float): 二阶矩估计的衰减率
        """
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon: float = 1e-8
        self.m = {}
        self.v = {}
        self.t = 0

    def update(self, params: Dict[str, np.array], grads: Dict[str, np.array]):
        """
        更新参数
        Args:
            params (dict): 模型参数
            grads (dict): 梯度
        """
        self.t += 1
        for key in params.keys():
            if key not in self.m:
                self.m[key] = np.zeros_like(params[key])
                self.v[key] = np.zeros_like(params[key])
            self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grads[key]
            self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * (grads[key] ** 2)
            m_hat = self.m[key] / (1 - self.beta1**self.t)
            v_hat = self.v[key] / (1 - self.beta2**self.t)
            params[key] -= self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
