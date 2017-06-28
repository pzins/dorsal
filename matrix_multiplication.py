import os
import sys
import tensorflow as tf
import time
import socket
from tensorflow.python.client import timeline
import numpy as np

host = socket.gethostname()

start_time = time.time()
n = 2048
dtype = tf.float32


with tf.device("/cpu:0"):
    x = tf.placeholder(tf.float32, [None, 2000], name="x_images")


    W = tf.Variable(tf.random_normal([2000, 1000], stddev=0.35),name="W_weights")
    # a = tf.Variable(tf.random_normal([100, 100], stddev=0.35),name="x_input")
    a = np.random.randint(255, size=(1000, 2000))



    product = tf.matmul(x, W)


sess = tf.Session()
run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
run_metadata = tf.RunMetadata()

sess.run(tf.global_variables_initializer())
for i in range(1000):
    res = sess.run(product, feed_dict={x: a})
res = sess.run(product, feed_dict={x: a}, options=run_options, run_metadata=run_metadata)


elapsed_time = time.time() - start_time
print("Elapsed time :", elapsed_time)
# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format()
with open('trace_' + __file__[:-3] + "_" + host + '.json', 'w') as f:
        f.write(ctf)
