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
from keras.layers import Dense
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

    df = mongodb_read(c.STUDY_COL)
    df = df.sort_values(by="time")
    df = df.reset_index()

    # parameter毎に順序切り替え
    if parameter == c.CLOSE:
        df = df.ix[:, ["time","close","open","high","low","volume","fiveave","tenave","fiftave",'tma5','tma10',
             'tma15','ema5','ema10','ema15','dema5','dema10','dema15',
             'tema5','tema10','tema15','wma5','wma10','wma15','trend',
             'bbands5up','bbands5mid','bbands5low','bbands10up','bbands10mid',
             'bbands10low','bbands15up','bbands15mid','bbands15low',
             'rocp5','rocp10','rocp15','mom5','mom10','mom15','rsi5','rsi10',
             'rsi15','MACD','MACDsig','MACDhist','apo5','apo10','apo15',
             'ppo5','ppo10','ppo15','cmo5','cmo10','cmo15']]
        prm = ["close"]
    if parameter == c.FIVEAVE:
        df = df.ix[:, ["time", "fiveave", "close","open","high","low","volume","tenave","fiftave",'tma5','tma10',
             'tma15','ema5','ema10','ema15','dema5','dema10','dema15',
             'tema5','tema10','tema15','wma5','wma10','wma15','trend',
             'bbands5up','bbands5mid','bbands5low','bbands10up','bbands10mid',
             'bbands10low','bbands15up','bbands15mid','bbands15low',
             'rocp5','rocp10','rocp15','mom5','mom10','mom15','rsi5','rsi10',
             'rsi15','MACD','MACDsig','MACDhist','apo5','apo10','apo15',
             'ppo5','ppo10','ppo15','cmo5','cmo10','cmo15']]
        prm = ["fiveave"]
    if parameter == c.TENAVE:
        df = df.ix[:, ["time", "tenave","close","open","high","low","volume","fiveave","fiftave",'tma5','tma10',
             'tma15','ema5','ema10','ema15','dema5','dema10','dema15',
             'tema5','tema10','tema15','wma5','wma10','wma15','trend',
             'bbands5up','bbands5mid','bbands5low','bbands10up','bbands10mid',
             'bbands10low','bbands15up','bbands15mid','bbands15low',
             'rocp5','rocp10','rocp15','mom5','mom10','mom15','rsi5','rsi10',
             'rsi15','MACD','MACDsig','MACDhist','apo5','apo10','apo15',
             'ppo5','ppo10','ppo15','cmo5','cmo10','cmo15']]
        prm = ["tenave"]
    if parameter == c.FIFTAVE:
        df = df.ix[:, ["time", "fiftave","close","open","high","low","volume","fiveave","tenave",'tma5','tma10',
             'tma15','ema5','ema10','ema15','dema5','dema10','dema15',
             'tema5','tema10','tema15','wma5','wma10','wma15','trend',
             'bbands5up','bbands5mid','bbands5low','bbands10up','bbands10mid',
             'bbands10low','bbands15up','bbands15mid','bbands15low',
             'rocp5','rocp10','rocp15','mom5','mom10','mom15','rsi5','rsi10',
             'rsi15','MACD','MACDsig','MACDhist','apo5','apo10','apo15',
             'ppo5','ppo10','ppo15','cmo5','cmo10','cmo15']]
        prm = ["fiftave"]

    print(parameter + "についての時系列データに並べ替えしました")

    # 一番左の列を１日分移動上に(prmの位置はデータによるので要注意)
    df_shift = df.copy()
    df_shift[prm] = df_shift[prm].shift(-1)

    # 求めたいものを得るための素材を１つ
    df_test = df.tail(1)

    # 念のためデータをdf_2として新しいデータフレームへコピー
    # 加工元のデータを変えないようにするための措置
    df_2 = df_shift.copy()

    # 最後尾はいらないので除去
    lastnum = len(df_2) - 1  # データ行数を求める（個数　-　1）で最後行を見つける
    df_2 = df_2.drop(lastnum)  # データの最後尾を削除する
    # time(時間)を消去
    del df_2["time"]
    del df_test["time"]
    df_2 = df_2.astype(np.float32)
    df_test = df_test.astype(np.float32)

    return df_2, df_test

def LSTM2prediction():

    df,df_test = predictionDataMaker(c.CLOSE)
    # df = df[-2600:]
    # df = df.reset_index()
    # データセットの行数と列を格納
    n = df.shape[0]  # 行
    p = df.shape[1]  # 列


    # 訓練データとテストデータへ切り分け
    train_start = 0
    train_end = int(np.floor(n))  # 前から数えて行全体の〇割を教師データとして扱う

    data_train = df[train_start:train_end]  # トレーニングの幅の設定
    data_test = df_test

    # データの正規化
    scaler = MinMaxScaler(feature_range=(-1, 1))  # -1から1の範囲に正規化する設定
    scaler.fit(df[-260:])  # 教師データを元に正規化設定（テストデータは必要ない）

    # norm→ノーマライゼーション（正規化の略称）
    data_train_norm = scaler.transform(data_train)  # 教師データの正規化
    data_test_norm = scaler.transform(data_test)  # テストデータの正規化

    # 特徴量とターゲットへ切り分け
    X_train = data_train_norm[:, 1:]  # 説明関数（出力を求める素材）    列   0   1    2    3   4
    X_test = data_test_norm[:, 1:]  # closeを除く他の要素を選択している(close,open,high,low,volume)
    Y_train = data_train_norm[:, 0]  # 目的関数（出力を予想する）


    # reshapeを戻す時用の値の保存
    res = X_train.shape[1]
    # 学習機に入れるための配列加工
    X_train = np.reshape(X_train, (X_train.shape[0],1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0],1, X_test.shape[1]))



    # 設定
    epochs = 100           # 反復数（エポック数）
    batche_size = 1        # バッチサイズ
    earlyStopping = EarlyStopping(monitor= "val_loss",
                                  mode="auto",
                                  patience=20,
                                  min_delta=0,
                                  verbose=0
                                  )      # Val_lossの値が改善しなくなった時の学習打ち切り閾値

    # LSTMのモデルを設定
    # modelをトレーニングデータに合わせて構築
    n_in_size = X_train.shape[1]         # 入力の要素数
    n_out_size = 1                       # 出力の数
    dropout = 0.25                       # ドロップアウト
    optimizer = Adam(lr = 0.001)         # 最適化関数と学習率
    n_hidden = 256                       # 隠れ層のニューロン数
    activation = PReLU(alpha_initializer='random_normal', alpha_regularizer=None, alpha_constraint=None, shared_axes=None)

    # モデル構築
    model = Sequential()

    model.add(LSTM(256,
                   input_shape=(1,X_train.shape[-1]),
                   activation="relu",
                   recurrent_initializer="random_normal",
                   use_bias=True,
                   bias_initializer="random_normal",
                   dropout=dropout,
                   recurrent_dropout=dropout,
                   kernel_initializer = "random_normal",
                   return_sequences=True
                   ))

    model.add(LSTM(128,
                   # input_shape=(1,X_train.shape[-1]),
                   activation="relu",
                   dropout=dropout
                   ))

    model.add(Dense(n_out_size))


    model.compile(loss="mse",
                  optimizer= optimizer,
                  metrics=["accuracy"])

    hist =  model.fit(X_train,
                      Y_train,
                      batch_size= batche_size,
                      epochs = epochs,
                      callbacks=[earlyStopping],
                      )



    # 予測結果
    pre = model.predict(X_test,batch_size=batche_size)
    X_test = np.reshape(X_test, (X_test.shape[0], res))
    pre = np.concatenate([pre, X_test], 1)
    predicted = scaler.inverse_transform(pre)
    result = predicted[0][0]

    return result

#
if __name__ == "__main__":
    prediction = LSTM2prediction()
    print(prediction)

#     df = predictionDataMaker(c.CLOSE)
#
#     df_copy = df.copy()
#     # データセットの行数と列を格納
#     n = df.shape[0]  # 行
#     p = df.shape[1]  # 列
#
#
#     # 訓練データとテストデータへ切り分け
#     train_start = 0
#     train_end = int(np.floor(n * 0.99))  # 前から数えて行全体の８割を教師データとして扱う
#     # train_end = int(n - 1)
#     test_start = train_end   # 教師データ以降のデータをテストデータとして扱う
#     test_end = n
#     data_train = df[train_start:train_end]  # トレーニングの幅の設定
#     data_test = df[test_start:test_end]  # テストの幅の設定
#
#     checkdf = df_copy[test_start:test_end]  # 比較のために元の値のままの奴を隔離
#     checkdf = checkdf.iloc[:,0]
#     checkdf = checkdf.reset_index()
#
#
#     # データの正規化
#     scaler = MinMaxScaler(feature_range=(-1, 1))  # -1から1の範囲に正規化する設定
#     # scaler.fit(data_test)  # 教師データを元に正規化設定
#     scaler.fit(df[-260:])
#
#     # norm→ノーマライゼーション（正規化の略称）
#     data_train_norm = scaler.transform(data_train)  # 教師データの正規化
#     data_test_norm = scaler.transform(data_test)  # テストデータの正規化
#
#     # 特徴量とターゲットへ切り分け
#     X_train = data_train_norm[:, 1:]  # 説明関数（出力を求める素材）    列   0   1    2    3   4
#     X_test = data_test_norm[:, 1:]  # closeを除く他の要素を選択している(close,open,high,low,volume)
#     Y_train = data_train_norm[:, 0]  # 目的関数（出力を予想する）
#     Y_test = data_test_norm[:, 0]  # DataFrame中の一番左だけを選択している
#
#     # reshapeを戻す時用の値の保存
#     res = X_train.shape[1]
#     # 学習機に入れるための配列加工
#     X_train = np.reshape(X_train, (X_train.shape[0],1, X_train.shape[1]))
#     X_test = np.reshape(X_test, (X_test.shape[0],1, X_test.shape[1]))
#
#
#
#     # 設定
#     epochs = 100           # 反復数（エポック数）
#     batche_size = 1        # バッチサイズ
#     earlyStopping = EarlyStopping(monitor= "val_loss",
#                                   mode="auto",
#                                   patience=20,
#                                   min_delta=0,
#                                   verbose=0
#                                   )      # Val_lossの値が改善しなくなった時の学習打ち切り閾値
#
#     # LSTMのモデルを設定
#     # modelをトレーニングデータに合わせて構築
#     n_in_size = X_train.shape[1]         # 入力の要素数
#     n_out_size = 1                       # 出力の数
#     dropout = 0.25                       # ドロップアウト
#     optimizer = Adam(lr = 0.001)         # 最適化関数と学習率
#     n_hidden = 256                       # 隠れ層のニューロン数
#     activation = PReLU(alpha_initializer='random_normal', alpha_regularizer=None, alpha_constraint=None, shared_axes=None)
#
#     # モデル構築
#     model = Sequential()
#
#     model.add(LSTM(256,
#                    input_shape=(1,X_train.shape[-1]),
#                    activation="relu",
#                    recurrent_initializer="random_normal",
#                    use_bias=True,
#                    bias_initializer="random_normal",
#                    dropout=dropout,
#                    recurrent_dropout=dropout,
#                    kernel_initializer = "random_normal",
#                    return_sequences=True
#                    ))
#
#     model.add(LSTM(128,
#                    # input_shape=(1,X_train.shape[-1]),
#                    activation="relu",
#                    dropout=dropout
#                    ))
#
#     model.add(Dense(n_out_size))
#
#
#     model.compile(loss="mse",
#                   optimizer= optimizer,
#                   metrics=["accuracy"])
#
#     hist =  model.fit(X_train,
#                       Y_train,
#                       batch_size= batche_size,
#                       epochs = epochs,
#                       callbacks=[earlyStopping],
#                       )
#
#     # 損失のグラフ化
#     loss = hist.history['loss']
#     epochs = len(loss)
#     plt.rc('font', family='serif')
#     fig = plt.figure()
#     fig.patch.set_facecolor('white')
#     plt.plot(range(epochs), loss, marker='.', label='loss(training data)')
#     plt.show()
#
#
#     # 予測結果
#     pre = model.predict(X_test,batch_size=batche_size)
#     X_test = np.reshape(X_test, (X_test.shape[0],res))
#     pre = np.concatenate([pre, X_test], 1)
#     # pre = pd.DataFrame(pre)
#     # pre = Y_train.append(pre)
#     predicted = scaler.inverse_transform(pre)
#     result = pd.DataFrame(predicted)
#     # Y_test = np.reshape(Y_test,(Y_test.shape[0],1))
#     # Y_test = np.concatenate([Y_test, X_test], 1)
#     # Y_test = scaler.inverse_transform(Y_test)
#     # Y_test = pd.DataFrame(Y_test)
#     plt.figure()
#     ax = result.iloc[:,0].plot()
#     # Y_test.iloc[:,0].plot(ax= ax)
#     checkdf.iloc[:, 1].plot(ax= ax)
#     plt.show()
#     # print(predicted[-1,0])
#

