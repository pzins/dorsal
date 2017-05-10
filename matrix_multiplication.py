import os
import sys
import tensorflow as tf
import time
import socket
from tensorflow.python.client import timeline


host = socket.gethostname()

start_time = time.time()
n = 2048
dtype = tf.float32


mA = tf.Variable(tf.ones((n, n), dtype=dtype))
mB = tf.Variable(tf.ones((n, n), dtype=dtype))


product = tf.matmul(mA, mB)


sess = tf.Session()
run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
run_metadata = tf.RunMetadata()

sess.run(tf.global_variables_initializer())
res = sess.run(product, options=run_options, run_metadata=run_metadata)
print(res)
elapsed_time = time.time() - start_time
print("Elapsed Time :", elapsed_time)
# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format()
with open('trace_matrix_multiplication' + "_" + host + '.json', 'w') as f:
        f.write(ctf)
