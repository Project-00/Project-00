# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import tensorflow as tf
import os.path
import csv
import scipy
import matplotlib.pyplot as plt
import tflearn

from sklearn import datasets

# ファイルパスの宣言
csv_path = './USDJPY.csv'


#正規化
def seikika(key):
    #keyに正規化したいデータを渡して正規化して値を返す
    key -= np.min(np.abs(key))
    key /= np.max(np.abs(key))

    return key

#高値と安値のデータから各日付の平均データを作る
#おまけ程度
def midRate():
    #高値のデータ抽出
    highValue = pd.read_csv(csv_path,
                          usecols=["高値"],
                          engine='python')
    HighValue = highValue.values
    HighValue = HighValue.astype("float32")

    #安い値のデータ抽出
    lowValue = pd.read_csv(csv_path,
                          usecols=["安値"],
                          engine='python')
    LowValue = lowValue.values
    LowValue = LowValue.astype("float32")

    #高値安値の配列すべての平均データ
    MidRate = np.array(HighValue) + np.array(LowValue)
    MidRate /= 2

    return MidRate

#終値のデータを取得
def endValue():
    endValue = pd.read_csv(csv_path,
                          usecols=["終値"],
                          engine='python')
    EndValue = endValue.values
    EndValue = EndValue.astype("float32")

    return EndValue

#終値の差分を求めてる
def differentEndValue():

    end = endValue()
    end = np.array(end,dtype="float32")

    Diff = np.diff(end)

    return Diff


#正解データの分類について
# 論理値を用いたベクトルを生成したい
# 例として、要素数２、内容は上々、上下、下上、下々としてそれぞれに１か０の値を与える。
# 与える基準として終値の差分に論理値を与えたとして
# 次にTrueを獲得している場合に１
# 次にFalseと変動している場合に0
# 値段が上がるパターンを正解として記録したい
def Vector():

    diff = differentEndValue()

    diff = np.array(diff,dtype="float32")
    #求めた差分について真偽値、0<の時に1、0>の時に0を与える。
    vector = np.all([x > 0 for x in diff])
    vector = np.array(vector,dtype="float32")
    Vector_data = []

    #Vector_dataを作る
    for Vec in vector:
        #vectorが偽、即ち0<の時
        if vector < 0:
            #vectorの次の配列が偽、即ち下々の時
            if np.roll(vector,1) < 0:
                Vec = [0]
                Vector_data.append(Vec)
            else:
                Vec = [1]
                Vector_data.append(Vec)

        #vectorが真、即ち0>の時
        else:
            #vectorの次の配列が偽、即ち上下の時
            if np.roll(vector,1) < 0:
                Vec = [0]
                Vector_data.append(Vec)
            else:
                Vec = [1]
                Vector_data.append(Vec)

    return Vector_data

#目的変数の生成
def Purpose(Y):
    #目的変数の箱はY値
    Y = np.array([])

if __name__ == "__main__":

    #実験
    #高値のデータ抽出
    highValue = pd.read_csv(csv_path,
                          usecols=["高値"],
                          engine='python')
    HighValue = highValue.values
    HighValue = HighValue.astype("float32")

    startValue = pd.read_csv(csv_path,
                            usecols=["始値"],
                            engine='python')
    StartValue = startValue.values
    StartValue = StartValue.astype("float32")

    #安い値のデータ抽出
    lowValue = pd.read_csv(csv_path,
                          usecols=["安値"],
                          engine='python')
    LowValue = lowValue.values
    LowValue = LowValue.astype("float32")

    End = endValue()
    Mid = midRate()
    End = seikika(End)
    Mid = seikika(Mid)

    High = seikika(HighValue)
    Low = seikika(LowValue)
    Start = seikika(StartValue)
    # #
    # #相関係数を求める
    # mean = np.array([0,0])
    End = np.array(End,dtype="float32")
    Mid = np.array(Mid,dtype="float32")
    High = np.array(High,dtype="float32")
    Low = np.array(Low,dtype="float32")
    Start = np.array(Start,dtype="float32")
    #
    # Corrcoef = np.corrcoef(End,Mid,True)

    #結合
    dataset = np.c_[Start,High,Mid,Low]
    dataset = np.array(dataset,dtype="float32")
    # Vector_data = Vector()

    #説明変数を抽出
    x_vals = np.array([x[0:4] for x in dataset])
    #目的変数を抽出
    y_vals = np.array([x[0] for x in End])

    #データセットをトレーニングセットとテストセットに分割
    train_indices = np.random.choice(len(x_vals),round(len(x_vals)*0.8),replace=False)

    test_indices = np.array(list(set(range(len(x_vals))) - set(train_indices)))
    x_vals_train = x_vals[train_indices]
    x_vals_test = x_vals[test_indices]
    y_vals_train = y_vals[train_indices]
    y_vals_test = y_vals[test_indices]

    #書籍パクリのために一応記述正規化
    def normalaize_cols(m):
        col_max = m.max(axis=0)
        col_min = m.min(axis=0)
        return (m - col_min) / (col_max - col_min)

    #上のdefを使ってnp型の正規化表現
    x_vals_train = np.nan_to_num(normalaize_cols(x_vals_train))
    x_vals_test = np.nan_to_num(normalaize_cols(x_vals_test))


    sess = tf.Session()


    #バッチサイズ
    batch_size = 30
    #プレースホルダーの設定
    x_data = tf.placeholder(shape=[None,4],dtype=tf.float32)
    y_target = tf.placeholder(shape=[None,1],dtype=tf.float32)

    #変数の定義を作成
    def init_variable(shape):
        return(tf.Variable(tf.random_normal(shape = shape)))

    #ロジスティック層の定義を作成
    def logistic(input_layer, multiplication_weight, bias_weight, activation=True):

        liner_layer = tf.add(tf.matmul(input_layer,multiplication_weight), bias_weight)

        #シグモイド関数の利用　0~1の挙動を示す関数　確率で使用する
        if activation:
            return (tf.nn.sigmoid(liner_layer))
        else:
            return (liner_layer)


    #ニューラルネットを用いた層の形成(３層型）
    #１つ目のロジスティック層(４個の入力→１４個の隠れノード)
    A1 = init_variable(shape=[4,14])
    b1 = init_variable(shape=[14])
    logistic_layer1 = logistic(x_data, A1,b1)

    #２つ目のロジスティック層(16個→8個）
    A2 = init_variable(shape=[14,5])
    b2 = init_variable(shape=[5])
    logistic_layer2 = logistic(logistic_layer1, A2, b2)

    #３つ目のロジスティック層（8→1）
    A3 = init_variable(shape=[5,1])
    b3 = init_variable(shape=[1])
    final_output = logistic(logistic_layer2, A3, b3, activation=False)

    #損失関数（交差エントロピー）と最適化関数を設定し、変数を初期化
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=final_output, labels=y_target))

    #最適化関数を作成
    my_opt = tf.train.AdamOptimizer(learning_rate= 0.001)
    train_step = my_opt.minimize(loss)

    #変数を初期化
    init = tf.global_variables_initializer()
    sess.run(init)

    #これまでのモデルと比較
    prediction = tf.round(tf.nn.sigmoid(final_output))
    prediction_correct = tf.cast(tf.equal(prediction, y_target), tf.float32)

    accuracy = tf.reduce_mean(prediction_correct)


    #損失ベクトルと正解ベクトルの初期化
    loss_vec = []
    train_acc = []
    test_acc = []

    for i in range(3000):
        #バッチを選択するためのインデックスをランダムに選択
        rand_index =np.random.choice(len(x_vals_train), size = batch_size)

        #ランダムな値でバッチを取得
        rand_x = x_vals_train[rand_index]
        rand_y = np.transpose([y_vals_train[rand_index]])

        #トレーニングステップを実行
        sess.run(train_step, feed_dict={
            x_data: rand_x, y_target: rand_y
        })

        #トレーニングセットの損失値を取得
        temp_loss = sess.run(accuracy, feed_dict={
            x_data: rand_x, y_target:rand_y
        })
        #append追加
        loss_vec.append(temp_loss)

        #トレーニングセットの正解率を取得
        temp_acc_train = sess.run(accuracy,feed_dict={
            x_data: x_vals_train, y_target: np.transpose([y_vals_train])
        })
        #append追加
        train_acc.append(temp_acc_train)

        #テストセットの正解率を取得
        temp_acc_test = sess.run(accuracy, feed_dict={
            x_data: x_vals_test, y_target: np.transpose([y_vals_test])
        })
        test_acc.append(temp_acc_test)

        if (i+1)%150 == 0:
            print("Loss = " + str(temp_loss))

    #
    # #損失率のプロット
    # plt.plot(loss_vec, "k-")
    # plt.title("Cross Entropy Loss per cov")
    # plt.xlabel("Mid cov End")
    # plt.ylabel("Cross Entropy")
    # plt.show()
    #
    # #トレーニングセットとテストセットのプロット
    # plt.plot(train_acc, "r-", label="Train Set Accuracy")
    # plt.plot(test_acc, "b-", label="test Set Accuracy")
    # plt.title("Train and Test")
    # plt.xlabel("Mid cov End")
    # plt.ylabel("updown")
    # plt.legend(loc="lower right")
    # plt.show()

    saver = tf.train.Saver()
    saver.save(sess, './testmodel')