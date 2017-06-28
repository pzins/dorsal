import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.client import timeline
import socket
import time

host = socket.gethostname()
start_time = time.time()

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


# Parameters
learning_rate = 0.01
training_epochs = 10
batch_size = 500
display_step = 1

# tf Graph Input
x = tf.placeholder(tf.float32, [None, 784], name="x_images") # mnist data image of shape 28*28=784
y = tf.placeholder(tf.float32, [None, 10], name="y_labels") # 0-9 digits recognition => 10 classes

# Set model weights
W = tf.Variable(tf.zeros([784, 10]), name="W_weights")
b = tf.Variable(tf.zeros([10]), name="b_bias")

# Construct model
pred = tf.nn.softmax(tf.matmul(x, W, name="matmul_x_W") + b, name="softmax_x_W_b") # Softmax

# Minimize error using cross entropy
cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred, name="pred_log"), reduction_indices=1, name="reduce_sum_y_log_pred"))
# Gradient Descent
optimizer = tf.train.RMSPropOptimizer(learning_rate, name="optimizer").minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()


# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE, output_partition_graphs=True)
    run_metadata = tf.RunMetadata()

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys}, options=run_options, run_metadata=run_metadata)

            # Compute average loss
            avg_cost += c / total_batch

        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))

elapsed_time = time.time() - start_time
print("Elapsed time :", elapsed_time)
# Create the Timeline object, and write it to a json
tl = timeline.Timeline(run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format(show_memory=True)
sess.close()
with open('trace_' + __file__[:-3] + "_" + host + '.json', 'w') as f:
        f.write(ctf)
