import abc
import numpy as np
from typing import List, Dict, Literal
from pydantic import BaseModel
from collections import OrderedDict

from libs.layers import (
    Layer,
    AffineLayer,
    ReluLayer,
    SigmoidLayer,
    SoftmaxWithLossLayer,
    BatchNormalizationLayer,
    DropoutLayer,
    ConvolutionLayer,
    PoolingLayer,
)
from libs.functions import numerical_gradient

ActivationType = Literal['relu', 'sigmoid']
WeightScaleType = Literal['he', 'xavier', float]


class Network(abc.ABC):
    @abc.abstractmethod
    def predict(self, x: np.ndarray, train_flg: bool = False) -> np.ndarray:
        """
        前向传播，计算输出
        Args:
            x (np.ndarray): 输入数据
            train_flg (bool, optional): 是否处于训练模式。默认为 False。

        Returns:
            np.ndarray: 网络输出
        """
        pass

    @abc.abstractmethod
    def loss(self, x: np.ndarray, t: np.ndarray, train_flg: bool = False) -> float:
        """
        计算损失
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据
            train_flg (bool, optional): 是否处于训练模式。默认为 False。

        Returns:
            float: 损失值
        """
        pass

    @abc.abstractmethod
    def accuracy(self, x: np.ndarray, t: np.ndarray) -> float:
        """
        计算准确率
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据

        Returns:
            float: 准确率
        """
        pass

    @abc.abstractmethod
    def gradient(self, x: np.ndarray, t: np.ndarray) -> Dict[str, np.ndarray]:
        """
        计算梯度(反向传播)
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据

        Returns:
            Dict[str, np.ndarray]: 各参数的梯度
        """
        pass


class NeuralNet(Network):
    """多层神经网络类
    该类实现了一个多层前馈神经网络，支持多种激活函数、批归一化、Dropout等功能。
    """

    def __init__(
        self,
        input_size: int,
        hidden_size_list: List[int],
        output_size: int,
        activation: ActivationType = 'relu',
        weight_scale: WeightScaleType = 'he',
        use_batchnorm: bool = False,
        weight_decay_lambda: float = 0.0,
        use_dropout: bool = False,
        dropout_ration: float = 0.5,
        verbose: bool = True,
    ) -> None:
        """
        初始化多层神经网络

        Args:
            input_size (int): 输入层大小
            hidden_size_list (List[int]): 隐藏层大小列表
            output_size (int): 输出层大小
            activation (ActivationType, optional): 激活函数类型，支持 'relu', 'sigmoid'默认值为 'relu'。
            weight_scale (str | float, optional): 权重初始化的缩放因子或方法。可以是 'he', 'xavier' 或具体的浮点数值(0-1)。默认值为 he
            use_batchnorm (bool, optional): 是否使用批归一化。默认值为 False。
            weight_decay_lambda (float, optional): 权重衰减系数。为0时不生效, 默认值为 0
            use_dropout (bool, optional): 是否使用Dropout。默认值为 False。
            dropout_ration (float, optional): Dropout比率，介于0和1之间。默认值为0.5。
        """
        self.input_size = input_size
        self.hidden_size_list = hidden_size_list
        self.output_size = output_size
        self.activation = activation
        self.weight_scale = weight_scale
        self.use_batchnorm = use_batchnorm
        self.weight_decay_lambda = weight_decay_lambda
        self.use_dropout = use_dropout
        self.dropout_ration = dropout_ration
        self.verbose = verbose

        self.params = {}
        self.layers: Dict[str, Layer] = OrderedDict()
        self.last_layer: Layer = None

        self._init_layers()

    def _get_weight_scale(self, idx: int) -> float:
        """
        获取权重缩放因子

        Args:
            idx (int): 层索引

        Returns:
            float: 权重缩放因子
        """
        if isinstance(self.weight_scale, str):
            if self.weight_scale == 'he':
                return np.sqrt(2.0 / self.hidden_size_list[idx - 1])
            elif self.weight_scale == 'xavier':
                return np.sqrt(1.0 / self.hidden_size_list[idx - 1])
            else:
                raise ValueError(f"Unsupported weight scale: {self.weight_scale}")
        else:
            return self.weight_scale

    def _add_affine_layer(self, idx: int, input_size: int, output_size: int):
        """
        添加全连接层

        Args:
            idx (int): 层索引
            input_size (int): 输入大小
            output_size (int): 输出大小
        """
        W_key = f'W{idx+1}'
        b_key = f'b{idx+1}'
        layer_name = f'Affine{idx+1}'
        if self.verbose:
            print(
                f"\t【全连接层】: {layer_name}, {W_key}({input_size}:{output_size}), {b_key}({output_size})"
            )
        weight_scale_value = self._get_weight_scale(idx)
        self.params[W_key] = np.random.randn(input_size, output_size) * weight_scale_value
        self.params[b_key] = np.zeros(output_size)
        self.layers[layer_name] = AffineLayer(self.params[W_key], self.params[b_key])

    def _add_batchnorm_layer(self, idx: int, output_size: int):
        """
        添加批归一化层

        Args:
            idx (int): 层索引
            output_size (int): 输出大小
        """
        layer_name = f'BatchNorm{idx+1}'
        if self.verbose:
            print(f"\t【批归一化层】: {layer_name}")
        gamma = np.ones(output_size)
        beta = np.zeros(output_size)
        self.params[f'gamma{idx+1}'] = gamma
        self.params[f'beta{idx+1}'] = beta
        self.layers[layer_name] = BatchNormalizationLayer(gamma, beta)

    def _add_activation_layer(self, idx: int):
        """
        添加激活层

        Args:
            idx (int): 层索引
        Raises:
            ValueError: 如果激活函数不支持
        """
        if self.activation == 'relu':
            layer_name = f'Relu{idx+1}'
            self.layers[layer_name] = ReluLayer()
        elif self.activation == 'sigmoid':
            layer_name = f'Sigmoid{idx+1}'
            self.layers[layer_name] = SigmoidLayer()
        else:
            raise ValueError(f"Unsupported activation function: {self.activation}")
        if self.verbose:
            print(f"\t【激活层】: {layer_name}")

    def _add_dropout_layer(self, idx: int):
        """
        添加Dropout层

        Args:
            idx (int): 层索引
        """
        layer_name = f'Dropout{idx+1}'
        if self.verbose:
            print(f"\t【Dropout层】比率: {self.dropout_ration}")
        self.layers[layer_name] = DropoutLayer(self.dropout_ration)

    def _init_layers(self):
        """
        初始化网络层
        Raises:
            ValueError: 如果激活函数不支持
        """
        all_size_list = [self.input_size] + self.hidden_size_list + [self.output_size]
        self.hidden_layer_num = len(self.hidden_size_list)
        if self.verbose:
            print("网络结构:")

        for idx in range(self.hidden_layer_num):
            # 添加全连接层
            self._add_affine_layer(idx, all_size_list[idx], all_size_list[idx + 1])

            # 添加批归一化层
            if self.use_batchnorm:
                self._add_batchnorm_layer(idx, all_size_list[idx + 1])

            # 添加激活层
            self._add_activation_layer(idx)

            # 添加Dropout层
            if self.use_dropout:
                self._add_dropout_layer(idx)

        # 添加最后的全连接层
        self._add_affine_layer(self.hidden_layer_num, all_size_list[-2], all_size_list[-1])
        if self.verbose:
            print("\t【Softmax + Loss】")
        self.last_layer = SoftmaxWithLossLayer()

    def predict(self, x: np.ndarray, train_flg: bool = False) -> np.ndarray:
        """
        前向传播，计算输出
        Args:
            x (np.ndarray): 输入数据
            train_flg (bool, optional): 是否处于训练模式。默认为 False。

        Returns:
            np.ndarray: 网络输出
        """
        for layer in self.layers.values():
            if isinstance(layer, BatchNormalizationLayer) or isinstance(layer, DropoutLayer):
                x = layer.forward(x, train_flg=train_flg)
            else:
                x = layer.forward(x)
        return x

    def loss(self, x: np.ndarray, t: np.ndarray, train_flg: bool = False) -> float:
        """
        计算损失
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据
            train_flg (bool, optional): 是否处于训练模式。默认为 False。

        Returns:
            float: 损失值
        """
        y = self.predict(x, train_flg)
        loss = self.last_layer.forward(y, t)

        # 权值衰减损失
        if self.weight_decay_lambda > 0:
            # 计算权重衰减损失
            weight_decay_loss = 0.0
            for key, value in self.params.items():
                if 'W' in key:
                    W = value
                    weight_decay_loss += 0.5 * self.weight_decay_lambda * np.sum(W**2)
            loss += weight_decay_loss
        return loss

    def accuracy(self, x: np.ndarray, t: np.ndarray) -> float:
        """
        计算准确率
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据

        Returns:
            float: 准确率
        """
        y = self.predict(x, train_flg=False)
        y = np.argmax(y, axis=1)
        if t.ndim != 1:
            t = np.argmax(t, axis=1)

        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy

    def numerical_gradient(self, x: np.ndarray, t: np.ndarray) -> Dict[str, np.ndarray]:
        """
        计算梯度(数值梯度)
        通过数值方法计算梯度，适用于小规模数据集或调试阶段
        这种方法计算梯度的速度较慢，但可以验证反向传播的实现是否正确。
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据

        Returns:
            Dict[str, np.ndarray]: 各参数的梯度
        """
        loss_W = lambda W: self.loss(x, t, train_flg=True)

        grads = {}
        for key in self.params.keys():
            grads[key] = numerical_gradient(loss_W, self.params[key])

        return grads

    def gradient(self, x: np.ndarray, t: np.ndarray) -> Dict[str, np.ndarray]:
        """
        计算梯度(反向传播)
        通过反向传播算法计算梯度，适用于大规模数据集
        这种方法计算梯度的速度较快，适用于实际训练阶段。
        Args:
            x (np.ndarray): 输入数据
            t (np.ndarray): 监督数据

        Returns:
            Dict[str, np.ndarray]: 各参数的梯度
        """
        # 前向传播
        self.loss(x, t, train_flg=True)

        # 反向传播
        dout = 1
        dout = self.last_layer.backward(dout)

        for layer in reversed(self.layers.values()):
            dout = layer.backward(dout)

        # 设置梯度
        grads = {}
        for idx in range(self.hidden_layer_num + 1):
            layer_name = f'Affine{idx+1}'
            if self.weight_decay_lambda > 0:
                # 添加权重衰减梯度
                grads[f'W{idx+1}'] = (
                    self.layers[layer_name].dW + self.weight_decay_lambda * self.params[f'W{idx+1}']
                )
            else:
                grads[f'W{idx+1}'] = self.layers[layer_name].dW
            grads[f'b{idx+1}'] = self.layers[layer_name].db

            if self.use_batchnorm and idx < self.hidden_layer_num:
                layer_name = f'BatchNorm{idx+1}'
                grads[f'gamma{idx+1}'] = self.layers[layer_name].dgamma
                grads[f'beta{idx+1}'] = self.layers[layer_name].dbeta

        return grads
