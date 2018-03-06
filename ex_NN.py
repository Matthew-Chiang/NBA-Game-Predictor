import numpy as np
import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
z
const = tf.constant(2.0,name = "const")

#b = tf.Variable(2.0,name = 'b')
b = tf.placeholder(tf.float32, [None, 1], name='b')
c = tf.Variable(1.0,name = 'c')

d = tf.add(b,c,name = 'd')
e = tf.add(c,const,name = 'e')
a = tf.multiply(d,e,name = 'a')

init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init_op)
    a_out = sess.run(a, feed_dict={b: np.arange(0, 10)[:, np.newaxis]})
    #a_out = sess.run(a)

    print("Variable a is {}".format(a_out))
