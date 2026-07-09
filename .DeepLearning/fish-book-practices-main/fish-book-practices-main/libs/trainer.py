import numpy as np
from libs.network import Network
from libs.optimizer import Optimizer, SGD, Momentum, AdaGrad, Adam


class Trainer:
    """训练器类，用于训练多层神经网络模型"""

    def __init__(
        self,
        network: Network,
        x_train: np.ndarray,
        t_train: np.ndarray,
        x_test: np.ndarray,
        t_test: np.ndarray,
        epochs=20,
        mini_batch_size=100,
        optimizer='sgd',
        optimizer_param={'lr': 0.01},
        evaluate_sample_num_per_epoch=None,
        verbose=True,
    ):
        """初始化训练器

        Args:
            network (Network): 需要训练的多层神经网络模型。
            x_train (np.ndarray): 训练数据。
            t_train (np.ndarray): 训练标签。
            x_test (np.ndarray): 测试数据。
            t_test (np.ndarray): 测试标签。
            epochs (int, optional): 训练的总轮数。默认为20。
            mini_batch_size (int, optional): 每个批次的样本数量。默认为100。
            optimizer (str, optional): 优化器类型，默认为'SGD'。
            optimizer_param (dict, optional): 优化器参数。默认为{'lr': 0.01}。
            evaluate_sample_num_per_epoch (int, optional): 每个epoch评估的样本数量。默认为None。
            verbose (bool, optional): 是否打印训练过程信息。默认为True。
        """
        self.network = network
        self.x_train = x_train
        self.t_train = t_train
        self.x_test = x_test
        self.t_test = t_test
        self.epochs = epochs
        self.batch_size = mini_batch_size
        self.evaluate_sample_num_per_epoch = evaluate_sample_num_per_epoch or len(x_train)
        self.verbose = verbose

        # 初始化优化器
        optimizer = optimizer.lower()
        if optimizer == 'sgd':
            self.optimizer = SGD(**optimizer_param)
        elif optimizer == 'momentum':
            self.optimizer = Momentum(**optimizer_param)
        elif optimizer == 'adagrad':
            self.optimizer = AdaGrad(**optimizer_param)
        elif optimizer == 'adam':
            self.optimizer = Adam(**optimizer_param)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer}")

        # 计算训练迭代次数
        self.train_size = x_train.shape[0]
        self.iter_per_epoch = max(self.train_size / mini_batch_size, 1)
        self.max_iter = int(epochs * self.iter_per_epoch)
        self.current_iter = 0
        self.current_epoch = 0

        # 初始化损失和准确率列表
        self.train_loss_list = []
        self.train_acc_list = []
        self.test_acc_list = []

    def train_step(self):
        """执行一次训练步骤"""
        # 随机选择一个批次的样本
        batch_mask = np.random.choice(self.train_size, self.batch_size)
        x_batch = self.x_train[batch_mask]
        t_batch = self.t_train[batch_mask]

        # 计算梯度
        grads = self.network.gradient(x_batch, t_batch)

        # 更新参数
        self.optimizer.update(self.network.params, grads)

        # 记录损失
        loss = self.network.loss(x_batch, t_batch)
        self.train_loss_list.append(loss)
        # if self.verbose:
        #     print("\ttrain loss:" + str(loss))

        if self.current_iter % self.iter_per_epoch == 0:
            self.current_epoch += 1

            x_train_sample, t_train_sample = self.x_train, self.t_train
            x_test_sample, t_test_sample = self.x_test, self.t_test
            if not self.evaluate_sample_num_per_epoch is None:
                t = self.evaluate_sample_num_per_epoch
                x_train_sample, t_train_sample = self.x_train[:t], self.t_train[:t]
                x_test_sample, t_test_sample = self.x_test[:t], self.t_test[:t]

            train_acc = self.network.accuracy(x_train_sample, t_train_sample)
            test_acc = self.network.accuracy(x_test_sample, t_test_sample)
            self.train_acc_list.append(train_acc)
            self.test_acc_list.append(test_acc)

            if self.verbose:
                print(
                    "epoch:"
                    + str(self.current_epoch)
                    + ", loss:"
                    + str(loss)
                    + ", train acc:"
                    + str(train_acc)
                    + ", test acc:"
                    + str(test_acc)
                )
        self.current_iter += 1

    def train(self):
        """开始训练"""
        if self.verbose:
            print("开始训练...")
        for i in range(self.max_iter):
            self.train_step()

        test_acc = self.network.accuracy(self.x_test, self.t_test)

        if self.verbose:
            print("=============== Final Test Accuracy ===============")
            print("test acc:" + str(test_acc))
