# -*- coding:utf8 -*-
import mongodb_write
from mongodb_read import mongodb_read
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import *
from mongodb_write import insertCollection
import const
import sys

# この関数を使うときは、USD_JPY_RATEの状態を最新状態にする必要がある。
# 順序的に言えば、USD_JPY_RATEの更新→平均の算出でなければ正確な値は出ない

c = sys.modules["const"]

# ２５日移動平均を求める関数
def twentyfiveAverage(key,df):
    # keyには要素日付呼び出し
    # twentyfiveaverage = mongodb_read()
    # twentyfiveaverage = twentyfiveaverage.sort_values(by="time")
    # twentyfiveaverage = twentyfiveaverage.reset_index()

    # 引数の日付から25日遡って25日分範囲指定
    twentyfiveaverage = df[key - 25:key]
    # closeの部分を取り出す
    twentyfiveaverage = twentyfiveaverage.close

    # 終値の平均を算出する処理
    result = twentyfiveaverage.mean()

    return result


# １０日移動平均を求める関数
def tenAverage(key,df):
    # keyには要素日付を呼び出し

    # １０日分の終値をUSD_JPY_RATEから取り出す処理
    # 読み込みと時刻昇順に並べ替え
    # tenaverage = mongodb_read()
    # tenaverage = tenaverage.sort_values(by="time")
    # tenaverage = tenaverage.reset_index()

    # 引数の日付から10日遡って10日分の範囲指定
    tenaverage = df[key - 10 : key]
    # closeの部分を取り出す
    tenaverage = tenaverage.close

    # 終値の平均を算出する処理(数字部分だけ)
    result = tenaverage.mean()

    return result

# ５日移動平均を求める関数
def fiveAverage(key,df):
    # dayには要素日付を入力
    # 引数の日付から、行を特定するための数

    # # ５日分の終値をUSD_JPY_RATEから取り出す処理
    # fiveaverage = mongodb_read()
    # fiveaverage = fiveaverage.sort_values(by="time")
    # fiveaverage = fiveaverage.reset_index()

    # 日付timeに対してその日から５日遡った値～timeまでの範囲を取得
    fiveaverage = df[key - 5 : key]
    fiveaverage = fiveaverage.close

    # 終値の平均を算出する処理
    result = fiveaverage.mean()

    return result



def MakeMovingAverage():

    # モンゴDBからtimeとcloseを取ってくる
    df = mongodb_read()
    df = df.sort_values(by="time")
    df = df.reset_index()
    df = df[["time","close"]]

    # 格納リスト作成
    fivelist = []
    tenlist = []
    twenlist = []

    # time毎に5日平均を回す！（前から５番目まで飛ぶ）
    for i in range(5,len(df)):

        Five = fiveAverage(i,df)

        # Five出力結果のリストの作成
        fivelist.append(Five)

    # 25日移動平均の要素数に合わせてデータを削除(20行分)
    del fivelist[:20]


    # time毎に10日平均を回す！（前から１０番目まで飛ぶ）
    for j in range(10,len(df)):

        Ten = tenAverage(j,df)

        # Ten出力結果のリストの作成
        tenlist.append(Ten)

    # 25日移動平均の要素数に合わせてデータを削除(15行分)
    del tenlist[:15]


    # time毎に25日平均を回す(前から２５番目まで飛ぶ)
    for k in range(25,len(df)):

        Twen = twentyfiveAverage(k,df)

        # Twen出力結果リストの作成
        twenlist.append(Twen)

    # 25日分のデータフレームを除去、timeだけ残す
    df = df.time
    dflist = df.tolist()
    del dflist[:25]

    # ２５日平均に数を合わせたので、辞書登録まわし
    for x in range(len(twenlist)):

        d = {"time":dflist[x] ,"fiveave":fivelist[x],"tenave":tenlist[x],"twenave":twenlist[x]}

        result = insertCollection(c.MOVINGAVERAGE_COL, d)

if __name__ == "__main__":

    collection = mongodb_write.getDBCollection(c.MOVINGAVERAGE_COL)
    collection.remove()
    result = MakeMovingAverage()

    # if文で3日前が5日>10日の時、5日<10日の時
    # if文で2日前が5>10,5<10の時
    # if文で1日前が5>10,5<10の時
    # 指定日の１０日平均と５日平均の差を見る


    # １０日平均と５日平均がどちらが上にきているか
    #     ５日平均が１０日平均より上にある場合
    #       さらに価格が５日平均よりうえなら