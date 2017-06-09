import tensorflow as tf
import numpy as np
"""
with tf.device("/cpu:0"):
    a = tf.random_normal([200, 300  ], mean=-1, stddev=4)
    b = tf.random_normal([200, 300], mean=-1, stddev=4)
    c = a+b
    s = tf.Session()
    print(s.run(c))
"""
x = tf.placeholder(tf.float32, [200, 300])
y = tf.placeholder(tf.float32, [200, 300])
z = tf.placeholder(tf.float32, [200, 300])

a = np.random.normal(0, 1, [200, 300])
b = np.random.normal(0, 1, [200, 300])
c = np.random.normal(0, 1, [200, 300])

# a = tf.random_normal([200, 3000], mean=-1, stddev=4)
# b = tf.random_normal([200, 3000], mean=-1, stddev=4)

s = tf.Session()

d = x+y+z
print(s.run(d, feed_dict={x: a, y: b, z: c}))

# c = a + b
# print(s.run(c))
