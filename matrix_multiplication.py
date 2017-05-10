import os
import sys
import tensorflow as tf
import time

start_time = time.time()
n = 2048
dtype = tf.float32


mA = tf.Variable(tf.ones((n, n), dtype=dtype))
mB = tf.Variable(tf.ones((n, n), dtype=dtype))


product = tf.matmul(mA, mB)


sess = tf.Session()

sess.run(tf.global_variables_initializer())
res = sess.run(product)
print(res)
elapsed_time = time.time() - start_time
print("Elapsed Time :", elapsed_time)
