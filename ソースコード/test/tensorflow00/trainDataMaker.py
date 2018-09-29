# -*- coding: utf-8 -*-
# ライブラリのインポート
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# -- 学習データ加工部分 --

def trainDataMaker(csvfile):
    # OANDAAPI のドル円１日足を取得して扱いやすくしたデータを用いているため注意。（要工夫）
    # CSVファイルの読み込み（）内で指定
    # 内容の順は time（時間） close（終） open（始） high（高） low（低） volume（取引数）　の順
    # 要素を増やすことでより精度が上がる模様
    df = pd.read_csv("./__csv__/" + csvfile)

    # 終値を１日分移動(closeの位置はデータによるので要注意)
    df_shift = df.copy()
    df_shift.close = df_shift.close.shift(-1)

    # 念のためデータをdf_2として新しいデータフレームへコピー
    # 加工元のデータを変えないようにするための措置
    df_2 = df_shift.copy()

    # 最後尾はいらないので除去
    lastnum = len(df_2) - 1  # データ行数を求める（個数　-　1）で最後行を見つける
    df_2 = df_2.drop(lastnum)
    # time(時間)を消去
    del df_2["time"]

    # データセットの行数と列を格納
    n = df_2.shape[0]  # 行
    p = df_2.shape[1]  # 列

    # 訓練データとテストデータへ切り分け
    train_start = 0
    train_end = int(np.floor(n * 0.8))  # 前から数えて行全体の８割を教師データとして扱う
    test_start = train_end + 1  # 教師データ以降のデータをテストデータとして扱う
    test_end = n
    data_train = df_2[train_start:train_end]  # トレーニングの幅の設定
    data_test = df_2[test_start:test_end]  # テストの幅の設定

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
    Y_test = data_test_norm[:, 0]  # closeだけを選択している

    return X_train, X_test, Y_train, Y_test, scaler

# 値の呼び出し方のメモ
# if __name__ == "__main__":
#     tdm = trainDataMaker("usd_jpy_api.csv")
#
#     X_train = tdm[0]
#     X_test = tdm[1]
#     Y_train = tdm[2]
#     Y_test = tdm[3]
#     scaler = tdm[4]
#
#     print(X_train)
#     print(X_test)
#     print(Y_train)
#     print(Y_test)
#     print(scaler)
