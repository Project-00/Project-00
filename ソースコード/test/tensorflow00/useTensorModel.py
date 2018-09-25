import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
# TensorFlowのセッション
sess = tf.Session()

# 訓練済みモデルのmetaファイル読み込み
saver = tf.train.import_meta_graph("tensor4.ckpt.meta")
# checkpointファイルから最新の学習モデルを選択
saver.restore(sess, tf.train.latest_checkpoint("./"))

# W_outとBias_outを復元（出力層の重みとバイアス）
graph = tf.get_default_graph()
weight = graph.get_tensor_by_name("weight:0")
bias = graph.get_tensor_by_name("bias:0")

#print(sess.run("weight:0"))
#print(sess.run("bias:0"))

# now?
now = np.array[99.919,100.471,99.887,30965]
pred = sess.run("weight:0") * now + sess.run("bias:0")

print(pred)

