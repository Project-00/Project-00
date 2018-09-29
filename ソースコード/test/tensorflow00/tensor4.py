# -*- coding: utf-8 -*-
# ライブラリのインポート
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
import tensorflow as tf
import os.path

# -- 学習データ加工部分 --

# OANDAAPI のドル円１日足を取得して扱いやすくしたデータを用いているため注意。（要工夫）
# CSVファイルの読み込み（）内で指定
# 内容の順は time（時間） close（終） open（始） high（高） low（低） volume（取引数）　の順
# 要素を増やすことでより精度が上がる模様
df = pd.read_csv("./__csv__/usd_jpy_api.csv")

# 終値を１日分移動
df_shift = df.copy()
df_shift.close = df_shift.close.shift(-1)

# 念のためデータをdf_2として新しいデータフレームへコピー
# 加工元のデータを変えないようにするための措置
df_2 = df_shift.copy()

# 最後尾はいらないので除去
lastnum = len(df_2) - 1     #データ行数を求める（個数　-　1）で最後行を見つける
df_2 = df_2.drop(lastnum)
# time(時間)を消去
del df_2["time"]

# データセットのサイズを確認
# print(df_2.shape[0])
# print(df_2.shape[1])
# print(df_2.tail())

# データセットの行数と列を格納
n = df_2.shape[0]   #行
p = df_2.shape[1]   #列

# 訓練データとテストデータへ切り分け
train_start = 0
train_end = int(np.floor(n * 0.8))    # 前から数えて行全体の８割を教師データとして扱う
test_start = train_end + 1          # 教師データ以降のデータをテストデータとして扱う
test_end = n
data_train = df_2[train_start:train_end]     # トレーニングの幅の設定
data_test = df_2[test_start:test_end]        # テストの幅の設定


# データの正規化
scaler = MinMaxScaler(feature_range=(-1,1))     # -1から1の範囲に正規化する設定
scaler.fit(data_train)                          # 教師データを元に正規化設定（テストデータは必要ない）

# norm→ノーマライゼーション（正規化の略称）
data_train_norm = scaler.transform(data_train)  # 教師データの正規化
data_test_norm = scaler.transform(data_test)    # テストデータの正規化

#特徴量とターゲットへ切り分け
X_train = data_train_norm[:, 1:]    # 説明関数（出力を求める素材）    列   0   1    2    3   4
X_test = data_test_norm[:, 1:]      # closeを除く他の要素を選択している(close,open,high,low,volume)
Y_train = data_train_norm[:, 0]     # 目的関数（出力を予想する）
Y_test = data_test_norm[:, 0]       # closeだけを選択している


# -- tensorflowのニューラルネットワーク構築 --

# 訓練データの説明関数を取得
n_stocks = X_train.shape[1]     # 説明関数の列数（close 等の要素の種類の数）

# ニューロンの数を設定（２層のニューラルネットワーク）（シンプル過ぎるから要修正点）
n_neurons_1 = 256
n_neurons_2 = 128

# セッションの開始
net = tf.InteractiveSession()

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

# 損失関数(誤差の計算)交差エントロピー
mse = tf.reduce_mean(tf.squared_difference(out,Y))

# 最適化関数
opt = tf.train.AdamOptimizer(name="opt").minimize(mse)

# 初期化
net.run(tf.global_variables_initializer())


# ニューラルネットワークの設定
batch_size = 128        # 同時に処理する数
mse_train = []          # 空箱にしておく(随時addしていくため）
mse_test = []           # 上に同じ

# 反復処理数
epochs = 500
for e in range(epochs):
    net.run(opt, feed_dict={X: X_train, Y: Y_train})


# -- テストデータで予測 --
pred_test = net.run(out, feed_dict={X: X_test})

# 予測値をテストデータに戻す（値も正規化から戻す）
pred_test = np.concatenate((pred_test.T, X_test), axis=1)
pred_inv = scaler.inverse_transform(pred_test)

# 予想結果の値はpred_inv
print(pred_inv)
# 読み方は左から close open high low vol



#訓練済みモデルの保存
cwd = os.getcwd()
saver = tf.train.Saver()
saver.save(net, cwd + "\\tensor4.ckpt")
print('Saved a model.')

net.close()