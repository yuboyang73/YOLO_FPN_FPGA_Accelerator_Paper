import sys, os
import time
import numpy as np
import pickle


sys.path.append(os.pardir)
sys.path.append(os.curdir)
from dataset.mnist import load_mnist


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def softmax(x):
    c = np.max(x)
    exp_x = np.exp(x - c)
    sum_exp_x = np.sum(exp_x)
    return exp_x / sum_exp_x


(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, flatten=True, one_hot_label=False)


def init_network():
    with open("./models/sample_weight.pkl", "rb") as f:
        network = pickle.load(f)

    return network


def predict(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)

    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)

    a3 = np.dot(z2, W3) + b3
    y = softmax(a3)

    return y


network = init_network()

batch_size = 100
time_start = time.time()
accuracy_cnt = 0
for i in range(0, len(x_test), batch_size):
    x_batch = x_test[i : i + batch_size]
    y_batch = predict(network, x_batch)
    print(y_batch.shape)
    p = np.argmax(y_batch, axis=1)
    print(p)
    accuracy_cnt += np.sum(p == t_test[i : i + batch_size])

time_end = time.time()
print(f"预测{len(x_test)}个样本用时：{time_end - time_start}秒")
print(f"准确率：{accuracy_cnt / len(x_test)}")
