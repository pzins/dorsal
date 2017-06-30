import tensorflow as tf
import numpy as np
import datetime
from tensorflow.python.client import timeline
import socket
import time

host = socket.gethostname()
now = datetime.datetime.now()

time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) \
       + "_" + str(now.hour) + "_" + str(now.minute)

run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE, output_partition_graphs=True)
run_metadata = tf.RunMetadata()

height = 10000
width = 10000

a = np.random.normal(0, 1, [height, width])
b = np.random.normal(0, 1, [height, width])
c = np.random.normal(0, 1, [height, width])
d = np.random.normal(0, 1, [height, width])

# with tf.device("/cpu:0"):
w = tf.placeholder(tf.float32, [height, width], name="w_placeholder")
x = tf.placeholder(tf.float32, [height, width], name="x_placeholder")
y = tf.placeholder(tf.float32, [height, width], name="y_placeholder")
z = tf.placeholder(tf.float32, [height, width], name="z_placeholder")
ww = tf.placeholder(tf.float32, [height, width], name="w_placeholder")
xx = tf.placeholder(tf.float32, [height, width], name="x_placeholder")
yy = tf.placeholder(tf.float32, [height, width], name="y_placeholder")
zz = tf.placeholder(tf.float32, [height, width], name="z_placeholder")
add1 = tf.add(w, x, "add1")
add2 = tf.add(y, z, "add2")
add3 = tf.add(ww, xx, "add3")
add4 = tf.add(yy, zz, "add4")
res2 = tf.add(add3, add4, "res2")
res1 = tf.add(add1, add2, "res1")
res = tf.matmul(res1, res2, name="res")



config = tf.ConfigProto()
config.inter_op_parallelism_threads = 10
config.intra_op_parallelism_threads = 4

logdir = "/home/pierre/Tensorboard/" + time
s = tf.Session(config=config)
merged = tf.summary.FileWriter(logdir, s.graph)



# print(s.run(res, feed_dict={w: a, x: b, y: c, z: d}))
print(s.run(res, feed_dict={w: a, x: c, y: b, z: d, ww: b, xx: a, yy: d, zz: c}, run_metadata=run_metadata, options=run_options))
# print(s.run(res, feed_dict={w: b, x: c, y: d, z: a}, run_metadata=run_metadata, options=run_options))


# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)
s.close()
with open('trace_' + __file__[:-3] + "_" + host + "_" + time + '.json', 'w') as f:
    f.write(ctf)
