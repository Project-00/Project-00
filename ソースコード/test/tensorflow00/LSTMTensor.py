import os
import re
import string
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os.path
import sys
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from keras.layers.advanced_activations import PReLU
from mongodb_read import mongodb_read

# 定数呼び出し
c = sys.modules["const"]

# LSTMのモデルを設定
def build_LSTMmodel(InputsData):
    n_in_size = InputsData.shape[1]      # len(Data)データの数
    n_out_size = 1                  # len(Y[0])
    n_hidden = 400                  # 隠れ層の数
    Input_length = 0                # 入力系列数
    dropout = 0.50                  # ドロップアウト


    model = Sequential()

    model.add(PReLU())
    model.add(LSTM(n_hidden,
                   batch_input_shape=(None, n_in_size, n_out_size),
                   return_sequences=True,
                   stateful=True))
    model.add(Dropout(dropout))
    model.add(Dense(units=250,activation=PReLU))
    model.add(Dropout(dropout))
    model.add(Dense(unit=150,activation=PReLU))
    model.add(Dropout(dropout))
    model.add(Dense(units=75,activation=PReLU))
    model.add(Dropout(dropout))
    model.add(Dense(units=150,activation=PReLU))
    model.add(Dropout(dropout))
    model.add(Dense(units=1,activation=PReLU))

    model.compile(loss="mean_squared_error",
                  optimizer="adam",
                  metrics=["accuracy"])
    return model


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

    # セッション開始の奴
    sess = tf.Session()

    # 設定
    hidden = 80             # 出力次元(75日移動平均を意識)
    epochs = 3000           # 反復数（エポック数）
    batche_size = 80        # バッチサイズ
    learning_rate = 0.001   # 学習率
    earlyStopping = 10      # Val_lossの値が改善しなくなった時の学習打ち切り閾値

    model = build_LSTMmodel()

    model.fit(X_train,
              Y_train,
              batch_size= batche_size,
              epochs = 3000,
              callbacks=[earlyStopping],
              validation_split= learning_rate
              )
    predicted = model.predict(X_test)


    # 保存と読み込み
    model.save("LSTM_test_model.h5")
    load_model = load_model("LSTM_test_model.h5")