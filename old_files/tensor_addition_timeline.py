import tensorflow as tf
import numpy as np
from tensorflow.python.client import timeline
import time
import socket

host = socket.gethostname()
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
run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE, output_partition_graphs=True)
run_metadata = tf.RunMetadata()
d = x+y+z
print(s.run(d, feed_dict={x: a, y: b, z: c}, options=run_options, run_metadata=run_metadata))
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)
# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)
s.close()
with open('trace_' + __file__[:-3] + "_" + host + '.json', 'w') as f:
    f.write(ctf)



# c = a + b
# print(s.run(c))
