import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
import tensorflow as tf
import os.path
import tensor4

cwd = os.getcwd()
# TensorFlowのセッション
sess = tf.Session()

# 訓練済みモデルのmetaファイル読み込み
saver = tf.train.import_meta_graph("tensor4.ckpt.meta")
# checkpointファイルから最新の学習モデルを選択
saver.restore(sess, tf.train.latest_checkpoint("./"))

# tensor4から使用する要素の復元
graph = tf.get_default_graph()
weight = graph.get_tensor_by_name("weight:0")
bias = graph.get_tensor_by_name("bias:0")
h1weight = graph.get_tensor_by_name("h1weight:0")
h1bias = graph.get_tensor_by_name("h1bias:0")
h2weight = graph.get_tensor_by_name("h2weight:0")
h2bias = graph.get_tensor_by_name("h2bias:0")
out = graph.get_tensor_by_name("out:0")



Xinput = [99.919,100.471,99.887,30965]

# -- 予測 --
pred_test = sess.run(out, feed_dict={Xinput})

# 予測値をテストデータに戻す（値も正規化から戻す）
pred_test = np.concatenate((pred_test.T, Xinput), axis=1)
pred_inv = scaler.inverse_transform(pred_test)

# 予想結果の値はpred_inv
print(pred_inv)
# 読み方は左から close open high low vol


print(pred_inv)

