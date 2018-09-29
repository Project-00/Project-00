import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
import tensorflow as tf
import os.path
from trainDataMaker import trainDataMaker
from testDataMaker import testDataMaker


cwd = os.getcwd()

# tdm = trainDataMaker("usd_jpy_api.csv")
tdm = testDataMaker("usd_jpy_api_test.csv")

scaler = tdm[4]

# 説明関数の要素数（列数）
n_stocks = tdm[5]

# 予測材料
X_input = tdm[1]


# tensor4から使用する要素の復元

# ニューロンの数
n_neurons_1 = 256
n_neurons_2 = 128

# プレースホルダーの作成
X = tf.placeholder(dtype=tf.float32, shape=[None, n_stocks], name="X")
Y = tf.placeholder(dtype=tf.float32, shape=[None], name="Y")

# 初期化
sigma = 1
weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
bias_initializer = tf.zeros_initializer()


# バイアスと隠れ層の重み
W_hidden_1 = tf.Variable(weight_initializer([n_stocks, n_neurons_1]), name="h1weight")
bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]), name="h1bias")
W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]), name="h2weight")
bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]), name="h2bias")

# 出力の重み
W_out = tf.Variable(weight_initializer([n_neurons_2, 1]), name="weight")
bias_out = tf.Variable(bias_initializer([1]), name="bias")


# 隠れ層の設定（ReLU＝活性化関数）
hidden_1 = tf.nn.leaky_relu(tf.add(tf.matmul(X, W_hidden_1),bias_hidden_1))

hidden_2 = tf.nn.leaky_relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))

# 出力層の設定
out = tf.transpose(tf.add(tf.matmul(hidden_2, W_out), bias_out))

# -- setting --

# TensorFlowのセッション
net = tf.InteractiveSession()

# 訓練済みモデルのmetaファイル読み込み
# saver = tf.train.import_meta_graph("tensor4.ckpt.meta")

saver = tf.train.Saver()
#  変数の読み込み
saver.restore(net, "tensor4.ckpt")



# -- 予測 --

pred_test = net.run(out, feed_dict={X: X_input})

# 予測値をテストデータに戻す（値も正規化から戻す）
pred_test = np.concatenate((pred_test.T, X_input), axis=1)
pred_inv = scaler.inverse_transform(pred_test)

# 予想結果の値はpred_inv
print(pred_inv)
# 読み方は左から close open high low vol





