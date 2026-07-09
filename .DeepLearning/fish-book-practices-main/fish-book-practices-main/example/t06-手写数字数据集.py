import sys, os
import numpy as np
from PIL import Image


sys.path.append(os.pardir)
sys.path.append(os.curdir)
from dataset.mnist import load_mnist

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=False, flatten=True, one_hot_label=False)

print(x_train.shape)
print(t_train.shape)
print(x_test.shape)
print(t_test.shape)


def img_show(img):
    pil_img = Image.fromarray(np.uint8(img))
    pil_img.show()


label = t_train[0]
print("label=", label)

img = x_train[0]
img = img.reshape(28, 28)
img_show(img)
