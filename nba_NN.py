import numpy as np
import tensorflow as tf

learning = 0.5
epochs = 10
batchSize = 100

#training placeholders

x = tf.placeholder(tf.float32,[None,312])
y = tf.placeholder(tf.float32,[None,2])

# declaring weights and biases

# connecting input to first layer
W1 = tf.Variable(tf.random_normal([312, 200], stddev=0.03), name='W1')
b1 = tf.Variable(tf.random_normal([200]), name='b1')

# connecting first to second layer
W2 = tf.Variable(tf.random_normal([200, 100], stddev=0.03), name='W2')
b2 = tf.Variable(tf.random_normal([100]), name='b2')

# connecting second to output layer
W3 = tf.Variable(tf.random_normal([100, 2], stddev=0.03), name='W3')
b3 = tf.Variable(tf.random_normal([2]), name='b3')

#forward prop

#input to first layer
hidden_one = tf.add(tf.matmul(x,W1),b1)
hidden_one = tf.nn.relu(hidden_one)

#first to second layer
hidden_two = tf.add(tf.matmul(W1,W2),b2)
hidden_two = tf.nn.relu(hidden_two)

#output layer
y_ = tf.nn.softmax(tf.add(tf.matmul(hidden_two,W3),b3))

#clipping the output for back propagation
y_clipped = tf.clip_by_value(y_,1e-10,0.9999999)

#define cost function
cost_func = tf.reduce_mean(tf.reduce_sum(y*tf.log(y_clipped) + (1-y) * tf.log(1-y_clipped),axis=1))

#optimizer
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning).minimize(cost_func)

#initalization optimizer
init_op = tf.global_variables_initializer()


# define an accuracy assessment operation
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# dataSet = 1225 rows,  312 cols
#learning = 0.5
#epochs = 10
#batchSize = 100

#starting Session

trainingSet = np.genfromtxt("DataSets/trainingSet.csv",delimiter=',', dtype="float32")
labels = np.genfromtxt("Labels/trainingSet.csv",delimiter=',', dtype="float32")
print (type(trainingSet[0][0]))


sliceSet= tf.data.Dataset.from_tensor_slices((trainingSet, labels))
Set = tf.data.Dataset.from_tensor_slices(sliceSet)

testEx = np.genfromtxt("DataSets/testingSet.csv",delimiter=',', dtype="float32")
testLb = np.genfromtxt("Labels/testingSet.csv",delimiter=',', dtype="float32")


with tf.Session() as sess:
    sess.run(init_op)
    total_batch = int(len(trainingSet)/batchSize)

    for epoch in range(epochs):
        avg_cost = 0
        for i in range(total_batch):
            batch_x,batch_y = Set.train.next_batch(batch_size = batchSize)
            _, c = sess.run([optimizer,cost_func],
                            feed_dict={x: batch_x, y: batch_y})
            avg_cost += c / total_batch
            print("Epoch:", (epoch + 1), "cost =", "{:.3f}".format(avg_cost))
    print(sess.run(accuracy, feed_dict={x: testEx, y: testLb }))
