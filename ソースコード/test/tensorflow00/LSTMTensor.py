import os
import re
import string
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import os.path
import sys
import const
from keras.models import Sequential
from keras.layers.core import Activation, Dense
from keras.layers.recurrent import LSTM
from keras.layers import Dropout
from keras.models import load_model
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from keras.layers.advanced_activations import PReLU
from keras.optimizers import Adam
from mongodb_read import mongodb_read

# 定数呼び出し
c = sys.modules["const"]


# -- 学習データ加工部分 --

def predictionDataMaker(parameter):
    # OANDAAPI のドル円１日足を取得して扱いやすくしたデータを用いているため注意。（要工夫）
    # CSVファイルの読み込み（）内で指定
    # 内容の順は time（時間） close（終） open（始） high（高） low（低） volume（取引数）　の順
    # 要素を増やすことでより精度が上がる模様
    # df = pd.read_csv("./__csv__/" + csvfile)

    df = mongodb_read(c.STUDY_COL)
    df = df.sort_values(by="time")
    df = df.reset_index()

    # parameter毎に順序切り替え
    if parameter == c.CLOSE:
        df = df.ix[:, ["time", "close", "open", "high", "low", "volume", "fiveave", "tenave", "fiftave"]]
        prm = ["close"]
    if parameter == c.OPEN:
        df = df.ix[:, ["time", "open", "close", "high", "low", "volume", "fiveave", "tenave", "fiftave"]]
        prm = ["open"]
    if parameter == c.HIGH:
        df = df.ix[:, ["time", "high", "close", "open", "low", "volume", "fiveave", "tenave", "fiftave"]]
        prm = ["high"]
    if parameter == c.LOW:
        df = df.ix[:, ["time", "low", "close", "open", "high", "volume", "fiveave", "tenave", "fiftave"]]
        prm = ["low"]
    if parameter == c.FIVEAVE:
        df = df.ix[:, ["time", "fiveave", "close", "open", "high", "volume", "low", "tenave", "fiftave"]]
        prm = ["fiveave"]
    if parameter == c.TENAVE:
        df = df.ix[:, ["time", "tenave", "close", "open", "high", "volume", "low", "fiveave", "fiftave"]]
        prm = ["tenave"]
    if parameter == c.FIFTAVE:
        df = df.ix[:, ["time", "fiftave", "close", "open", "high", "volume", "low", "fiveave", "tenave"]]
        prm = ["fiftave"]

    print(parameter + "を計算します")

    # df_test = df.tail(1)

    # 一番左の列を１日分移動上に(prmの位置はデータによるので要注意)
    df_shift = df.copy()
    df_shift[prm] = df_shift[prm].shift(-1)

    # 念のためデータをdf_2として新しいデータフレームへコピー
    # 加工元のデータを変えないようにするための措置
    df_2 = df_shift.copy()

    # 最後尾はいらないので除去
    lastnum = len(df_2) - 1  # データ行数を求める（個数　-　1）で最後行を見つける
    df_2 = df_2.drop(lastnum)  # データの最後尾を削除する
    # time(時間)を消去
    del df_2["time"]
    # del df_test["time"]

    # データセットの行数と列を格納
    n = df_2.shape[0]  # 行
    p = df_2.shape[1]  # 列

    # 訓練データとテストデータへ切り分け
    train_start = 0
    train_end = int(np.floor(n * 0.8))  # 前から数えて行全体の８割を教師データとして扱う
    test_start = train_end   # 教師データ以降のデータをテストデータとして扱う
    test_end = n
    data_train = df_2[train_start:train_end]  # トレーニングの幅の設定
    data_test = df_2[test_start:test_end]  # テストの幅の設定
    # data_train = df_2
    # data_test = df_test  # テストの幅の設定

    # データの正規化
    scaler = MinMaxScaler(feature_range=(-1, 1))  # -1から1の範囲に正規化する設定
    scaler.fit(data_train)  # 教師データを元に正規化設定（テストデータは必要ない）

    # norm→ノーマライゼーション（正規化の略称）
    data_train_norm = scaler.transform(data_train)  # 教師データの正規化
    data_test_norm = scaler.transform(data_test)  # テストデータの正規化

    # 特徴量とターゲットへ切り分け
    X_train = data_train_norm[:, 1:]  # 説明関数（出力を求める素材）    列   0   1    2    3   4
    X_test = data_test_norm[:, 1:]  # closeを除く他の要素を選択している(close,open,high,low,volume)
    Y_train = data_train_norm[:, 0]  # 目的関数（出力を予想する）
    Y_test = data_test_norm[:, 0]  # DataFrame中の一番左だけを選択している

    # 訓練データの説明関数を取得
    n_stocks = X_train.shape[1]  # 説明関数の列数（close 等の要素の種類の数）

    return X_train, X_test, Y_train, Y_test, scaler, n_stocks


# parameterの中身 OPEN:始値 CLOSE:終値 HIGH:高値 LOW:安値
def makePredictionModel(parameter):

    pdm = predictionDataMaker(parameter)

    X_train = pdm[0]    # 説明教師データ群
    X_test = pdm[1]     # 説明テストデータ群
    Y_train = pdm[2]    # 目的教師データ群
    Y_test = pdm[3]     # 目的テストデータ群
    scaler = pdm[4]     # 値を戻す時に使う（スカラ倍）
    n_stocks = pdm[5]   # 要素数
    
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # 設定
    epochs = 1           # 反復数（エポック数）
    batche_size = 1        # バッチサイズ
    earlyStopping = EarlyStopping(monitor= "val_loss",
                                  mode="auto",
                                  patience=20,
                                  min_delta=0,
                                  verbose=0
                                  )      # Val_lossの値が改善しなくなった時の学習打ち切り閾値

    # LSTMのモデルを設定
    # modelをトレーニングデータに合わせて構築
    n_in_size = X_train.shape[1]        # 入力の要素数
    n_out_size = 1                       # 出力の数
    dropout = 0.50                       # ドロップアウト
    optimizer = Adam(lr = 0.001)         # 最適化関数と学習率
    n_hidden = 256                       # 隠れ層のニューロン数
    input_dim = 7                        # 出力次元
    activation = PReLU(alpha_initializer='zeros', alpha_regularizer=None, alpha_constraint=None, shared_axes=None)
    n_inputs = 1
    n_outputs = 1


    X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
    Y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])

    # モデル構築
    model = Sequential()

    model.add(LSTM(n_hidden,
                   batch_input_shape=(batche_size,n_in_size,input_dim),    # batch_size,timesteps,input_dim
                   activation=activation,
                   recurrent_activation=activation,
                   recurrent_initializer="zeros",
                   use_bias=True,
                   bias_initializer="zeros",
                   dropout=dropout,
                   recurrent_dropout=dropout,
                   kernel_initializer = "he_normal"))
    # model.add(Dense(75,input_shape=(None,256),activation=activation,kernel_initializer = "he_normal"))
    # model.add(Dropout(dropout))
    # model.add(Dense(128,input_shape=(None,75),activation=activation,kernel_initializer = "he_normal"))
    # model.add(Dropout(dropout))
    # model.add(Dense(75,input_shape=(None,128),activation=activation,kernel_initializer = "he_normal"))
    # model.add(Dropout(dropout))
    model.add(Dense(n_out_size,activation=activation,kernel_initializer = "he_normal"))

    model.compile(loss="mse",
                  optimizer= optimizer,
                  metrics=["accuracy"])

    hist =  model.fit(X_train,
                      Y_train,
                      batch_size= batche_size,
                      epochs = epochs,
                      callbacks=[earlyStopping],
                      )

    # 損失のグラフ化
    loss = hist.history['loss']
    epochs = len(loss)
    plt.rc('font', family='serif')
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    plt.plot(range(epochs), loss, marker='.', label='loss(training data)')
    plt.show()

    # 予測結果
    predicted = model.predict(X_test,batch_size=batche_size)
    # predicted = scaler.inverse_transform(predicted)
    result = pd.DataFrame(predicted)
    result.columns = ['predict']
    result['actual'] = Y_test
    result.plot()
    plt.show()

if __name__ == "__main__":
    makePredictionModel(c.CLOSE)