import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def softmax(x):
    c = np.max(x)
    exp_x = np.exp(x - c)
    sum_exp_x = np.sum(exp_x)
    return exp_x / sum_exp_x


def identity_function(x):
    return x


def init_network():
    networks = {}
    networks["W1"] = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])
    networks["B1"] = np.array([0.1, 0.2, 0.3])

    networks["W2"] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
    networks["B2"] = np.array([0.1, 0.2])

    networks["W3"] = np.array([[0.1, 0.3], [0.2, 0.4]])
    networks["B3"] = np.array([0.1, 0.2])

    return networks


def forward(networks, x):
    """
    前向传播(forward propagation)
    """
    W1, W2, W3 = networks["W1"], networks["W2"], networks["W3"]
    B1, B2, B3 = networks["B1"], networks["B2"], networks["B3"]

    a1 = np.dot(x, W1) + B1
    z1 = sigmoid(a1)

    a2 = np.dot(z1, W2) + B2
    z2 = sigmoid(a2)

    a3 = np.dot(z2, W3) + B3
    y = softmax(a3)

    return y


x = np.array([1.0, 0.5])
networks = init_network()
print(forward(networks, x))
