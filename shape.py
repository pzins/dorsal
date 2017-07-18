import tensorflow as tf
import numpy as np
from tensorflow.python.client import timeline


size = 1000

a = tf.placeholder(tf.float32, [size, size, size], name="placeholder")

data = np.random.normal(0,size, [size, size, size])

sh = tf.shape(a)

run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE, output_partition_graphs=True)
run_metadata = tf.RunMetadata()

s = tf.Session()

while True:
	print(s.run(sh, feed_dict={a: data}, run_metadata=run_metadata, options=run_options))
	break

# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)
s.close()
with open('trace_shape.json', 'w') as f:
    f.write(ctf)


