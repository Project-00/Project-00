# -*- coding:utf8 -*-
from mongodb_read import mongodb_read
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import *

# この関数を使うときは、USD_JPY_RATEの状態を最新状態にする必要がある。
# 順序的に言えば、USD_JPY_RATEの更新→平均の算出でなければ正確な値は出ない

# １０日移動平均を求める関数
def tenAverage(time):
    # keyには要素日付を呼び出し

    # １０日分の終値をUSD_JPY_RATEから取り出す処理
    # 読み込みと時刻昇順に並べ替え
    tenaverage = mongodb_read()
    tenaverage = tenaverage.sort_values(by="time")
    tenaverage = tenaverage.reset_index()
    # 日付ラベルから要素の番号を取り出す
    key = tenaverage.get_loc(time)
    # 引数の日付から10日遡って10日分の範囲指定
    tenaverage = tenaverage[key-10:key]
    # closeの部分を取り出す
    tenaverage = tenaverage.close

    # 終値の平均を算出する処理(数字部分だけ)
    tenaverage = tenaverage.mean()

    return tenaverage

# ５日移動平均を求める関数
def fiveAverage(time):
    # dayには要素日付を入力
    # 引数の日付から、行を特定するための数

    # ５日分の終値をUSD_JPY_RATEから取り出す処理
    fiveaverage = mongodb_read()
    fiveaverage = fiveaverage.sort_values(by="time")
    fiveaverage = fiveaverage.reset_index()
    key = fiveaverage.get_loc(time)
    fiveaverage = fiveaverage[key-5:key] # 最新のものが下にあるので下から取り出してる
    fiveaverage = fiveaverage.close

    # 終値の平均を算出する処理
    fiveaverage = fiveaverage.mean()

    return fiveaverage


# 移動平均のトレンド傾きを調べる関数。連続した線形を微分して、＋か－かで上昇傾向か下降傾向か調べる


# def unknown():
#
#     # 過去3日分の平均移動データを5日と10日のそれぞれを取ってくる
#     # if文で3日前が5日>10日の時、5日<10日の時
#     # if文で2日前が5>10,5<10の時
#     # if文で1日前が5>10,5<10の時
#     # 指定日の１０日平均と５日平均の差を見る
#
#
#     # １０日平均と５日平均がどちらが上にきているか
#     #     ５日平均が１０日平均より上にある場合
#     #       さらに価格が５日平均よりうえなら