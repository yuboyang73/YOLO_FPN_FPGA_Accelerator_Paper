import numpy as np


def smooth_curve(x):
    """用于使损失函数的图形变圆滑

    参考：http://glowingpython.blogspot.jp/2012/02/convolution-with-numpy.html
    """
    window_len = 11
    s = np.r_[x[window_len - 1 : 0 : -1], x, x[-1:-window_len:-1]]
    w = np.kaiser(window_len, 2)
    y = np.convolve(w / w.sum(), s, mode='valid')
    return y[5 : len(y) - 5]


def shuffle_dataset(x, t):
    """打乱数据集

    Parameters
    ----------
    x : 训练数据
    t : 监督数据

    Returns
    -------
    x, t : 打乱的训练数据和监督数据
    """
    permutation = np.random.permutation(x.shape[0])
    x = x[permutation, :] if x.ndim == 2 else x[permutation, :, :, :]
    t = t[permutation]

    return x, t


def shuffle_dataset_and_split_validation_dataset(x, t, val_ratio=0.2):
    """打乱数据集并分割验证集

    Parameters
    ----------
    x : 训练数据
    t : 监督数据
    val_ratio : 验证集占比

    Returns
    -------
    x_train, x_val, t_train, t_val : 打乱后的训练数据和验证数据
    """
    x, t = shuffle_dataset(x, t)
    validation_num = int(x.shape[0] * val_ratio)

    x_val = x[:validation_num]
    t_val = t[:validation_num]

    x_train = x[validation_num:]
    t_train = t[validation_num:]

    return x_train, x_val, t_train, t_val


def im2col(input_data, filter_h, filter_w, stride=1, pad=0):
    """将输入数据转换为列格式

    Parameters
    ----------
    input_data : 输入数据，形状为 (N, C, H, W)
    filter_h : 卷积核高度
    filter_w : 卷积核宽度
    stride : 步长
    pad : 填充

    Returns
    -------
    col : 转换后的列格式数据
    """
    N, C, H, W = input_data.shape
    out_h = (H + 2 * pad - filter_h) // stride + 1
    out_w = (W + 2 * pad - filter_w) // stride + 1

    img = np.pad(input_data, [(0, 0), (0, 0), (pad, pad), (pad, pad)], 'constant')
    col = np.zeros((N, C, filter_h, filter_w, out_h, out_w))

    for y in range(filter_h):
        y_max = y + stride * out_h
        for x in range(filter_w):
            x_max = x + stride * out_w
            col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N * out_h * out_w, -1)

    return col


def col2im(col, input_shape, filter_h, filter_w, stride=1, pad=0):
    """将列格式数据转换回图像格式

    Parameters
    ----------
    col : 列格式数据
    input_shape : 输入数据的形状 (N, C, H, W)
    filter_h : 卷积核高度
    filter_w : 卷积核宽度
    stride : 步长
    pad : 填充

    Returns
    -------
    img : 转换后的图像格式数据
    """
    N, C, H, W = input_shape
    out_h = (H + 2 * pad - filter_h) // stride + 1
    out_w = (W + 2 * pad - filter_w) // stride + 1

    img = np.zeros((N, C, H + 2 * pad + stride - 1, W + 2 * pad + stride - 1))

    col = col.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2)

    for y in range(filter_h):
        y_max = y + stride * out_h
        for x in range(filter_w):
            x_max = x + stride * out_w
            img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x]

    return img[:, :, pad : H + pad, pad : W + pad]
