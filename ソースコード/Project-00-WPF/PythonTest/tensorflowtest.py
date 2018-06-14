import tensorflow as tf

def x_plus_b(x, b):
    _x = tf.constant(x)
    _b = tf.constant(b)
    result = tf.add(_x, _b)
    return result


with tf.Session() as sess:
    result = sess.run([x_plus_b(25., 32.)])
    print(result)
 