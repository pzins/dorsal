import tensorflow as tf
import numpy as np
import datetime
from tensorflow.python.client import timeline
import socket
import time
import os

host = socket.gethostname()
now = datetime.datetime.now()

time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) \
       + "_" + str(now.hour) + "_" + str(now.minute)

run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE, output_partition_graphs=True)
run_metadata = tf.RunMetadata()

height = 10000
width = int(10000)

w = tf.placeholder(tf.float32, [height, width], name="w_placeholder")
x = tf.placeholder(tf.float32, [height, width], name="x_placeholder")
y = tf.placeholder(tf.float32, [height, width], name="y_placeholder")
z = tf.placeholder(tf.float32, [height, width], name="z_placeholder")
a = np.random.normal(0, 1, [height, width])
b = np.random.normal(0, 1, [height, width])
c = np.random.normal(0, 1, [height, width])
d = np.random.normal(0, 1, [height, width])
add1 = tf.add(w, x, "add1")
add2 = tf.add(y, z, "add2")
res = tf.add(add1, add2, "res")

logdir = "/home/pierre/Tensorboard/" + time
s = tf.Session()
merged = tf.summary.FileWriter(logdir, s.graph)

# print(s.run(res, feed_dict={w: a, x: b, y: c, z: d}))
print(s.run(res, feed_dict={w: a, x: c, y: b, z: d}, run_metadata=run_metadata, options=run_options))
# print(s.run(res, feed_dict={w: b, x: c, y: d, z: a}, run_metadata=run_metadata, options=run_options))


# tfprof file generation
output_dir = "/home/pierre/tfprof_gen/"
tf.train.write_graph(s.graph.as_graph_def(), output_dir, 'graph.pbtxt', as_text=True)
with tf.gfile.Open(os.path.join(output_dir, "run_meta"), "w") as f:
    f.write(run_metadata.SerializeToString())
tf.contrib.tfprof.tfprof_logger.write_op_log(s.graph, output_dir, op_log=None)
# end tfprof

exit(0)

# tfprof
# Print to stdout an analysis of the memory usage and the timing information
# broken down by operations.
opts = tf.contrib.tfprof.model_analyzer.PRINT_ALL_TIMING_MEMORY.copy()
opts['output'] = 'timeline:outfile=/home/pierre/aaaaa.json'
tf.contrib.tfprof.model_analyzer.print_model_analysis(
    tf.get_default_graph(),
    run_meta=run_metadata,
    tfprof_options=opts)
exit(0)



# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)
s.close()
with open('trace_' + __file__[:-3] + "_" + host + '.json', 'w') as f:
    f.write(ctf)

print("------------------------")
for partition_graph_def in run_metadata.partition_graphs:
    print(partition_graph_def)  # Contains all the nodes that ran on a single device
