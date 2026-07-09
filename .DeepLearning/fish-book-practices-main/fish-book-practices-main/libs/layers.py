import abc
import numpy as np
from libs.functions import sigmoid, softmax, cross_entropy_error
from libs.util import im2col, col2im


class Layer(abc.ABC):
    """
    基础层类
    """

    @abc.abstractmethod
    def forward(self, x):
        """
        前向传播
        """
        pass

    @abc.abstractmethod
    def backward(self, dout):
        """
        反向传播
        """
        pass


class ReluLayer(Layer):
    """
    ReLU层
    """

    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = x <= 0
        out = x.copy()
        out[self.mask] = 0

        return out

    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout

        return dx


class SigmoidLayer(Layer):
    """
    Sigmoid层
    """

    def __init__(self):
        self.out = None

    def forward(self, x):
        self.out = sigmoid(x)
        return self.out

    def backward(self, dout):
        dx = dout * (1.0 - self.out) * self.out
        return dx


class AffineLayer:
    """
    仿射层
    """

    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.x = None
        self.dW = None
        self.db = None

    def forward(self, x):
        self.original_x_shape = x.shape
        x = x.reshape(x.shape[0], -1)
        self.x = x
        out = np.dot(x, self.W) + self.b

        return out

    def backward(self, dout):
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)

        dx = dx.reshape(*self.original_x_shape)
        return dx


class SoftmaxWithLossLayer(Layer):
    """
    Softmax with Cross Entropy Loss
    """

    def __init__(self):
        self.y = None
        self.t = None

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)

        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        dx = (self.y - self.t) / batch_size

        return dx


class BatchNormalizationLayer(Layer):
    """
    批量归一化层
    该层用于对输入数据进行归一化处理, 以加速训练和提高模型性能。
    通过对每个批次的输入数据进行标准化处理, 使得每个特征的均值为0, 方差为1。
    该层包含可学习的参数gamma和beta, 用于缩放和偏移归一化后的数据。
    通过在训练过程中计算每个批次的均值和方差, 并在测试时使用移动平均的均值和方差来进行归一化处理。
    通过这种方式, 批量归一化层可以减少内部协变量偏移, 加速收敛, 并提高模型的泛化能力。
    """

    def __init__(self, gamma, beta, momentum=0.9, running_mean=None, running_var=None):
        """
        初始化批量归一化层
        :param gamma: 缩放参数
        :param beta: 偏移参数
        :param momentum: 动量, 用于更新移动平均的均值和方差
        :param running_mean: 测试时使用的平均值
        :param running_var: 测试时使用的方差
        """
        self.gamma = gamma
        self.beta = beta
        self.momentum = momentum
        self.input_shape = None  # Conv层的情况下为4维, 全连接层的情况下为2维

        # 测试时使用的平均值和方差
        self.running_mean = running_mean
        self.running_var = running_var

        # backward时使用的中间数据
        self.batch_size = None
        self.xc = None
        self.std = None
        self.dgamma = None
        self.dbeta = None

    def forward(self, x, train_flg=True):
        """

        Args:
            x (_type_): 输入数据, 形状为(N, D)或(N, C, H, W), 其中N为批次大小, D为特征维度, C为通道数, H和W为高度和宽度。
            train_flg (bool, optional): 训练标志, 指示是否处于训练模式。默认为True。
        """
        self.input_shape = x.shape
        if x.ndim != 2:
            N, C, H, W = x.shape
            x = x.reshape(N, -1)

        out = self.__forward(x, train_flg)

        return out.reshape(*self.input_shape)

    def __forward(self, x, train_flg):
        if self.running_mean is None:
            N, D = x.shape
            self.running_mean = np.zeros(D)
            self.running_var = np.zeros(D)

        if train_flg:
            mu = x.mean(axis=0)
            xc = x - mu
            var = np.mean(xc**2, axis=0)
            std = np.sqrt(var + 10e-7)
            xn = xc / std

            self.batch_size = x.shape[0]
            self.xc = xc
            self.xn = xn
            self.std = std
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * mu
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * var
        else:
            xc = x - self.running_mean
            xn = xc / ((np.sqrt(self.running_var + 10e-7)))

        out = self.gamma * xn + self.beta
        return out

    def backward(self, dout):
        if dout.ndim != 2:
            N, C, H, W = dout.shape
            dout = dout.reshape(N, -1)

        dx = self.__backward(dout)

        dx = dx.reshape(*self.input_shape)
        return dx

    def __backward(self, dout):
        dbeta = dout.sum(axis=0)
        dgamma = np.sum(self.xn * dout, axis=0)
        dxn = self.gamma * dout
        dxc = dxn / self.std
        dstd = -np.sum((dxn * self.xc) / (self.std * self.std), axis=0)
        dvar = 0.5 * dstd / self.std
        dxc += (2.0 / self.batch_size) * self.xc * dvar
        dmu = np.sum(dxc, axis=0)
        dx = dxc - dmu / self.batch_size

        self.dgamma = dgamma
        self.dbeta = dbeta

        return dx


class DropoutLayer(Layer):
    """
    Dropout层
    该层用于在训练过程中随机丢弃一部分神经元, 以减少过拟合。
    在训练时, 根据给定的dropout比率随机将一部分神经元的输出设为0。
    在测试时, 直接返回输入数据, 不进行任何操作。
    """

    def __init__(self, dropout_ration=0.5):
        self.dropout_ration = dropout_ration
        self.mask = None

    def forward(self, x, train_flg=True):
        if train_flg:
            self.mask = np.random.rand(*x.shape) > self.dropout_ration
            return x * self.mask
        else:
            return x

    def backward(self, dout):
        return dout * self.mask


class ConvolutionLayer(Layer):
    """
    卷积层
    该层用于对输入数据进行卷积操作, 以提取特征。
    包含可学习的权重和偏置参数, 并支持前向传播和反向传播。
    """

    def __init__(self, W, b, stride=1, pad=0):
        """初始化卷积层
        Args:
            W (_type_): 权重矩阵, 形状为(FN, C, FH, FW), 其中FN为滤波器数量, C为输入通道数, FH和FW为滤波器的高度和宽度。
            b (_type_): 偏置向量, 形状为(FN,), 其中F为滤波器数量。
            stride (int, optional): 卷积步长, 默认为1
            pad (int, optional): 填充大小, 默认为0
        """
        self.W = W
        self.b = b
        self.stride = stride
        self.pad = pad

        # 中间变量
        self.x = None

        # 权重和偏置的梯度
        self.dW = None
        self.db = None

    def _forward(self, x):
        """前向传播
        Args:
            x (_type_): 输入数据, 形状为(N, C, H, W), 其中N为批次大小, C为输入通道数, H和W为高度和宽度。
        Returns:
            _type_: 卷积操作后的输出数据, 形状为(N, FN, out_h, out_w), 其中FN为滤波器数量, out_h和out_w为输出的高度和宽度。
        """
        N, C, H, W = x.shape
        FN, _, FH, FW = self.W.shape

        # 计算输出尺寸
        out_h = (H + 2 * self.pad - FH) // self.stride + 1
        out_w = (W + 2 * self.pad - FW) // self.stride + 1

        # 填充输入数据
        x_padded = np.pad(x, ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad)), mode='constant')

        # 初始化输出数据
        out = np.zeros((N, FN, out_h, out_w))

        # 执行卷积操作
        for n in range(N):
            for fn in range(FN):
                for h in range(out_h):
                    for w in range(out_w):
                        h_start = h * self.stride
                        h_end = h_start + FH
                        w_start = w * self.stride
                        w_end = w_start + FW

                        out[n, fn, h, w] = (
                            np.sum(x_padded[n, :, h_start:h_end, w_start:w_end] * self.W[fn])
                            + self.b[fn]
                        )

        # 保存输入数据供反向传播使用
        self.x = x
        return out

    def forward(self, x):
        FN, C, FH, FW = self.W.shape
        N, C, H, W = x.shape
        out_h = 1 + int((H + 2 * self.pad - FH) / self.stride)
        out_w = 1 + int((W + 2 * self.pad - FW) / self.stride)

        col = im2col(x, FH, FW, self.stride, self.pad)
        col_W = self.W.reshape(FN, -1).T

        out = np.dot(col, col_W) + self.b
        out = out.reshape(N, out_h, out_w, -1).transpose(0, 3, 1, 2)

        self.x = x
        self.col = col
        self.col_W = col_W

        return out

    def _backward(self, dout):
        """反向传播
        Args:
            dout (_type_): 上一层的梯度, 形状为(N, FN, out_h, out_w), 其中N为批次大小, FN为滤波器数量, out_h和out_w为输出的高度和宽度。
        Returns:
            _type_: 输入数据的梯度, 形状为(N, C, H, W), 其中C为输入通道数, H和W为高度和宽度。
        """
        N, C, H, W = self.x.shape
        FN, _, FH, FW = self.W.shape
        out_h = dout.shape[2]
        out_w = dout.shape[3]

        # 初始化梯度
        dx = np.zeros_like(self.x)
        dW = np.zeros_like(self.W)
        db = np.zeros_like(self.b)

        # 填充输入数据
        x_padded = np.pad(
            self.x,
            ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad)),
            mode='constant',
        )

        # 为dx创建带填充的版本
        dx_padded = np.pad(
            dx,
            ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad)),
            mode='constant',
        )

        # 执行反向传播
        for n in range(N):
            for fn in range(FN):
                for h in range(out_h):
                    for w in range(out_w):
                        h_start = h * self.stride
                        h_end = h_start + FH
                        w_start = w * self.stride
                        w_end = w_start + FW

                        dW[fn] += x_padded[n, :, h_start:h_end, w_start:w_end] * dout[n, fn, h, w]
                        db[fn] += dout[n, fn, h, w]
                        dx_padded[n, :, h_start:h_end, w_start:w_end] += (
                            self.W[fn] * dout[n, fn, h, w]
                        )

        # 去除填充部分的梯度
        if self.pad > 0:
            dx = dx_padded[:, :, self.pad : -self.pad, self.pad : -self.pad]
        else:
            dx = dx_padded

        self.dW = dW
        self.db = db

        return dx

    def backward(self, dout):
        FN, C, FH, FW = self.W.shape
        dout = dout.transpose(0, 2, 3, 1).reshape(-1, FN)

        self.db = np.sum(dout, axis=0)
        self.dW = np.dot(self.col.T, dout)
        self.dW = self.dW.transpose(1, 0).reshape(FN, C, FH, FW)

        dcol = np.dot(dout, self.col_W.T)
        dx = col2im(dcol, self.x.shape, FH, FW, self.stride, self.pad)

        return dx


class PoolingLayer(Layer):
    """
    池化层
    该层用于对输入数据进行池化操作, 以减少特征图的尺寸。
    支持最大池化和平均池化, 并支持前向传播和反向传播。
    """

    def __init__(self, pool_h, pool_w, stride=1, pad=0):
        """初始化池化层
        Args:
            pool_h (int): 池化窗口的高度
            pool_w (int): 池化窗口的宽度
            stride (int, optional): 池化步长, 默认为1
            pad (int, optional): 填充大小, 默认为0
        """
        self.pool_h = pool_h
        self.pool_w = pool_w
        self.stride = stride
        self.pad = pad

        # 中间变量
        self.x = None

    def _forward(self, x):
        """前向传播
        Args:
            x (_type_): 输入数据, 形状为(N, C, H, W), 其中N为批次大小, C为输入通道数, H和W为高度和宽度。
        Returns:
            _type_: 池化操作后的输出数据, 形状为(N, C, out_h, out_w), 其中out_h和out_w为输出的高度和宽度。
        """
        N, C, H, W = x.shape

        # 计算输出尺寸
        out_h = (H + 2 * self.pad - self.pool_h) // self.stride + 1
        out_w = (W + 2 * self.pad - self.pool_w) // self.stride + 1

        # 填充输入数据
        x_padded = np.pad(x, ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad)), mode='constant')

        # 初始化输出数据
        out = np.zeros((N, C, out_h, out_w))

        # 执行池化操作
        for n in range(N):
            for c in range(C):
                for h in range(out_h):
                    for w in range(out_w):
                        h_start = h * self.stride
                        h_end = h_start + self.pool_h
                        w_start = w * self.stride
                        w_end = w_start + self.pool_w
                        out[n, c, h, w] = np.max(x_padded[n, c, h_start:h_end, w_start:w_end])
        self.x = x
        return out

    def forward(self, x):
        N, C, H, W = x.shape
        out_h = int(1 + (H + 2 * self.pad - self.pool_h) / self.stride)
        out_w = int(1 + (W + 2 * self.pad - self.pool_w) / self.stride)

        col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
        col = col.reshape(-1, self.pool_h * self.pool_w)

        arg_max = np.argmax(col, axis=1)
        out = np.max(col, axis=1)
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

        self.x = x
        self.arg_max = arg_max

        return out

    def _backward(self, dout):
        """反向传播
        Args:
            dout (_type_): 上一层的梯度, 形状为(N, C, out_h, out_w), 其中N为批次大小, C为输入通道数, out_h和out_w为输出的高度和宽度。
        Returns:
            _type_: 输入数据的梯度, 形状为(N, C, H, W), 其中H和W为高度和宽度。
        """
        N, C, H, W = self.x.shape
        out_h = dout.shape[2]
        out_w = dout.shape[3]

        # 初始化梯度
        dx = np.zeros_like(self.x)

        # 填充输入数据
        x_padded = np.pad(
            self.x,
            ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad)),
            mode='constant',
        )
        dx_padded = np.pad(
            dx,
            ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad)),
            mode='constant',
        )

        # 执行反向传播
        for n in range(N):
            for c in range(C):
                for h in range(out_h):
                    for w in range(out_w):
                        h_start = h * self.stride
                        h_end = h_start + self.pool_h
                        w_start = w * self.stride
                        w_end = w_start + self.pool_w

                        # 找到最大值的位置
                        max_idx = np.argmax(x_padded[n, c, h_start:h_end, w_start:w_end])
                        max_h = max_idx // self.pool_w + h_start
                        max_w = max_idx % self.pool_w + w_start

                        dx_padded[n, c, max_h, max_w] += dout[n, c, h, w]

        # 去除填充部分的梯度
        if self.pad > 0:
            dx = dx_padded[:, :, self.pad : -self.pad, self.pad : -self.pad]
        else:
            dx = dx_padded

        return dx

    def backward(self, dout):
        dout = dout.transpose(0, 2, 3, 1)

        pool_size = self.pool_h * self.pool_w
        dmax = np.zeros((dout.size, pool_size))
        dmax[np.arange(self.arg_max.size), self.arg_max.flatten()] = dout.flatten()
        dmax = dmax.reshape(dout.shape + (pool_size,))

        dcol = dmax.reshape(dmax.shape[0] * dmax.shape[1] * dmax.shape[2], -1)
        dx = col2im(dcol, self.x.shape, self.pool_h, self.pool_w, self.stride, self.pad)

        return dx
