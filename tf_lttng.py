import tensorflow as tf




a = tf.constant([[1,2],[3,4]])
b = tf.constant([[10,18],[25,23]])
c = tf.transpose(a)
d = tf.transpose(b)
e = tf.matmul(a,b)
f = tf.matmul(c,d)
g = tf.matmul(e, f)

s = tf.Session()
s.run(g)
