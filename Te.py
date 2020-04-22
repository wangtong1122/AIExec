import input_data
import tensorflow as tf
def main():
  mnist = input_data.read_data_sets("data/", one_hot=True)
  x = tf.compat.v1.placeholder("float", [None, 784])
  W = tf.Variable(tf.zeros([784,10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.nn.softmax(tf.matmul(x,W) + b)
  y_ = tf.compat.v1.placeholder("float", [None,10])
  cross_entropy = -tf.reduce_sum(y_*tf.math.log(y))
  train_step = tf.compat.v1.train.AdamOptimizer(0.001).minimize(cross_entropy)
  init = tf.compat.v1.global_variables_initializer()
  sess = tf.compat.v1.Session()
  sess.run(init)
  for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
  print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

def weight_variable(shape):
  initial = tf.random.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool2d(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
def neturalTest():
  mnist = input_data.read_data_sets("data/", one_hot=True)
  x = tf.compat.v1.placeholder("float", [None, 784])
  y_ = tf.compat.v1.placeholder("float", [None,10])
  W_conv1 = weight_variable([5, 5, 1, 32])
  b_conv1 = bias_variable([32])
  x_image = tf.reshape(x, [-1,28,28,1])
  h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
  h_pool1 = max_pool_2x2(h_conv1)

  W_conv2 = weight_variable([5, 5, 32, 64])
  b_conv2 = bias_variable([64])

  h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
  h_pool2 = max_pool_2x2(h_conv2)

  W_fc1 = weight_variable([7 * 7 * 64, 1024])
  b_fc1 = bias_variable([1024])

  h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
  rate = 1 - tf.compat.v1.placeholder("float")
  h_fc1_drop = tf.nn.dropout(h_fc1, rate)
  W_fc2 = weight_variable([1024, 10])
  b_fc2 = bias_variable([10])

  y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
  cross_entropy = -tf.reduce_sum(y_ * tf.math.log(y_conv))

  train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(cross_entropy)
  correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
  init = tf.compat.v1.global_variables_initializer()
  with tf.Session() as sess:
    sess.run(init)
    for i in range(20000):
      batch = mnist.train.next_batch(50)
      if i % 100 == 0:
          train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], rate:1})
          print("step %d, training accuracy %g" % (i, train_accuracy))
      train_step.run(feed_dict={x: batch[0], y_: batch[1], rate: 0.5})
    print("test accuracy %g" % accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, rate:1}))
if __name__ == '__main__':
    neturalTest()