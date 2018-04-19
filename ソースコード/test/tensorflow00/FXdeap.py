# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from collections import namedtuple
import datetime
import urllib.request, urllib.error, urllib.parse
import operator as op
import numpy as np
import pandas as pd
import tensorflow as tf
import argparse



def create_dataset():
    data = pd.read_csv(EX_NAME,
                          usecols=["日付","始値","高値","安値","終値"],
                          engine='python')

    closing_data = pd.DataFrame()
    closing_data = data['終値']
    closing_data = closing_data.fillna(method='ffill')

    log_return_data = pd.DataFrame()
    log_return_data['rate_of_change'] = np.log(closing_data / closing_data.shift())

    columns = []
    for up_or_down, operator in [('Up', op.ge), ('Down', op.lt)]:
        columns.append(up_or_down)
        log_return_data[up_or_down] = 0
        flag = operator(log_return_data['rate_of_change'], 0)
        log_return_data.ix[flag, up_or_down] = 1

    start_days = 1

    end_days = start_days + TRAIN_DAYS

    for days in range(start_days, end_days):
        columns.append('{}'.format(days))

    index_num = len(log_return_data) - TRAIN_DAYS

    training_test_data = pd.DataFrame(columns=columns)

    for i in range(TRAIN_DAYS + 2, index_num):
        values = {}

    for up_or_down in ['Up', 'Down']:
        values[up_or_down] = log_return_data[up_or_down].ix[i]

        for days in range(start_days, end_days):
            values[str(days)] = log_return_data['rate_of_change'].ix[i - days]

        training_test_data = training_test_data.append(values, ignore_index=True)

    predictors_tf = training_test_data[training_test_data.columns[2:]]

    classes_tf = training_test_data[training_test_data.columns[:2]]

    training_set_size = int(len(training_test_data) * 0.8)
    test_set_size = len(training_test_data) - training_set_size

    return Dataset(
        training_predictors_tf=predictors_tf[:training_set_size],
        training_classes_tf=classes_tf[:training_set_size],
        test_predictors_tf=predictors_tf[training_set_size:],
        test_classes_tf=classes_tf[training_set_size:]
    )


def tf_confusion_metrics(model, actual_classes, session, feed_dict):
    predictions = tf.argmax(model, 1)
    actuals = tf.argmax(actual_classes, 1)

    ones_like_actuals = tf.ones_like(actuals)
    zeros_like_actuals = tf.zeros_like(actuals)
    ones_like_predictions = tf.ones_like(predictions)
    zeros_like_predictions = tf.zeros_like(predictions)

    tp_op = tf.reduce_sum(
        tf.cast(
            tf.logical_and(
                tf.equal(actuals, ones_like_actuals),
                tf.equal(predictions, ones_like_predictions)
            ),
            "float32"
        )
    )

    tn_op = tf.reduce_sum(
        tf.cast(
            tf.logical_and(
                tf.equal(actuals, zeros_like_actuals),
                tf.equal(predictions, zeros_like_predictions)
            ),
            "float32"
        )
    )

    fp_op = tf.reduce_sum(
        tf.cast(
            tf.logical_and(
                tf.equal(actuals, zeros_like_actuals),
                tf.equal(predictions, ones_like_predictions)
            ),
            "float32"
        )
    )

    fn_op = tf.reduce_sum(
        tf.cast(
            tf.logical_and(
                tf.equal(actuals, ones_like_actuals),
                tf.equal(predictions, zeros_like_predictions)
            ),
            "float32"
        )
    )

    tp, tn, fp, fn = \
        session.run(
            [tp_op, tn_op, fp_op, fn_op],
            feed_dict
        )


    tpr = float(tp) / (float(tp) + float(fn))
    fpr = float(fp) / (float(tp) + float(fn))


    accuracy = (float(tp) + float(tn)) / (float(tp) + float(fp) + float(fn) + float(tn))

    recall = tpr
    precision = float(tp) / (float(tp) + float(fp))


    f1_score = (2 * (precision * recall)) / (precision + recall)


    print('Precision = ', precision)
    print('Recall = ', recall)
    print('F1 Score = ', f1_score)
    print('Accuracy = ', accuracy)


def Neural_net(dataset):
    '''Binary Classification with TensorFlow'''


    sess = tf.Session()

    # Define variables for the number of predictors and number of classes to remove magic numbers from our code.
    num_predictors = len(dataset.training_predictors_tf.columns)
    num_classes = len(dataset.training_classes_tf.columns)

    # Define placeholders for the data we feed into the process - feature data and actual classes.
    feature_data = tf.placeholder("float32", [None, num_predictors])
    actual_classes = tf.placeholder("float32", [None, num_classes])

    # Define a matrix of weights and initialize it with some small random values.
    weights = tf.Variable(tf.truncated_normal([num_predictors, num_classes], stddev=0.0001))
    biases = tf.Variable(tf.ones([num_classes]))

    # Define our model...
    # Here we take a softmax regression of the product of our feature data and weights.
    model = tf.nn.softmax(tf.matmul(feature_data, weights) + biases)

    # Define a cost function (we're using the cross entropy).
    cost = -tf.reduce_sum(actual_classes * tf.log(model))

    # Define a training step...
    # Here we use gradient descent with a learning rate of 0.01 using the cost function we just defined.
    training_step = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)

    init = tf.initialize_all_variables()
    sess.run(init)

    return Environ(
        sess=sess,
        model=model,
        actual_classes=actual_classes,
        training_step=training_step,
        dataset=dataset,
        feature_data=feature_data
    )


def Neural_net_with_Layers(dataset):
    '''Feed Forward Neural Net with Two Hidden Layers in TensorFlow'''


    sess1 = tf.Session()

    num_predictors = len(dataset.training_predictors_tf.columns)
    num_classes = len(dataset.training_classes_tf.columns)

    feature_data = tf.placeholder("float32", [None, num_predictors])
    actual_classes = tf.placeholder("float32", [None, 2])

    weights1 = tf.Variable(tf.truncated_normal([TRAIN_DAYS, 50], stddev=0.0001))
    biases1 = tf.Variable(tf.ones([50]))

    weights2 = tf.Variable(tf.truncated_normal([50, 25], stddev=0.0001))
    biases2 = tf.Variable(tf.ones([25]))

    weights3 = tf.Variable(tf.truncated_normal([25, 2], stddev=0.0001))
    biases3 = tf.Variable(tf.ones([2]))

    # This time we introduce a single hidden layer into our model...
    hidden_layer_1 = tf.nn.relu(tf.matmul(feature_data, weights1) + biases1)
    hidden_layer_2 = tf.nn.relu(tf.matmul(hidden_layer_1, weights2) + biases2)
    model = tf.nn.softmax(tf.matmul(hidden_layer_2, weights3) + biases3)

    cost = -tf.reduce_sum(actual_classes * tf.log(model))

    train_op1 = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)

    init = tf.initialize_all_variables()
    sess1.run(init)

    return Environ(
        sess=sess1,
        model=model,
        actual_classes=actual_classes,
        training_step=train_op1,
        dataset=dataset,
        feature_data=feature_data
    )


def train():
    correct_prediction = tf.equal(tf.argmax(environ.model, 1), tf.argmax(environ.actual_classes, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    write_log(0, environ.sess.run(
        accuracy,
        feed_dict={
            environ.feature_data: dataset.training_predictors_tf.values,
            environ.actual_classes: dataset.training_classes_tf.values.reshape(len(dataset.training_classes_tf.values),
                                                                               2)
        }
    ))

    for i in range(1, ITERATIONS + 1):
        environ.sess.run(
            environ.training_step,
            feed_dict={
                environ.feature_data: dataset.training_predictors_tf.values,
                environ.actual_classes: dataset.training_classes_tf.values.reshape(
                    len(dataset.training_classes_tf.values), 2)
            }
        )
        if i % 5000 == 0:
            print(i, environ.sess.run(
                accuracy,
                feed_dict={
                    environ.feature_data: dataset.training_predictors_tf.values,
                    environ.actual_classes: dataset.training_classes_tf.values.reshape(
                        len(dataset.training_classes_tf.values), 2)
                }
            ))
        if i % 100 == 0:
            write_log(i, environ.sess.run(
                accuracy,
                feed_dict={
                    environ.feature_data: dataset.training_predictors_tf.values,
                    environ.actual_classes: dataset.training_classes_tf.values.reshape(
                        len(dataset.training_classes_tf.values), 2)
                }
            ))

    feed_dict = {
        environ.feature_data: dataset.training_predictors_tf.values,
        environ.actual_classes: dataset.training_classes_tf.values.reshape(len(dataset.training_classes_tf.values), 2)
    }

    return feed_dict


def write_log(i, accuracy):
    f = open('log.txt', 'a')

    i = str(i).ljust(7)
    accuracy = '%s\n' % str(accuracy).ljust(13)

    f.write(i + accuracy)

    f.close()

if __name__ == "__main__":
    TRAIN_DAYS = 30
    ITERATIONS = 30000
    EX_NAME = "USDJPY.csv"

    Dataset = namedtuple('Dataset', 'training_predictors_tf training_classes_tf test_predictors_tf test_classes_tf')
    Environ = namedtuple('Environ', 'sess model actual_classes training_step dataset feature_data')


    dataset = create_dataset()
    # print (dataset.training_predictors_tf.describe())

    # environ = Neural_net(dataset)
    environ = Neural_net_with_Layers(dataset)

    feed_dict = train()

    tf_confusion_metrics(environ.model, environ.actual_classes, environ.sess, feed_dict)


