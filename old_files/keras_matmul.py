import keras.backend as K
import numpy as np

A = np.random.rand(10,500)
B = np.random.rand(500,6000)


x = K.variable(value=A)
y = K.variable(value=B)

z = K.dot(x,y)

for i in range(10):
    K.eval(z)
