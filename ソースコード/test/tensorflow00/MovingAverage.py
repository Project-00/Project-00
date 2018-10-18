# -*- coding:utf8 -*-
from mongodb_read import mongodb_read
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import *

# この関数を使うときは、USD_JPY_RATEの状態を最新状態にする必要がある。
# 順序的に言えば、USD_JPY_RATEの更新→平均の算出でなければ正確な値は出ない

# １０日移動平均を求める関数
def tenAverage():

    # １０日分の終値をUSD_JPY_RATEから取り出す処理
    tenaverage = mongodb_read()
    tenaverage = tenaverage.close
    tenaverage = tenaverage[:-10] # 最新のものが下にあるので下から取り出してる

    # 終値の平均を算出する処理(数字部分だけ)
    tenaverage = tenaverage.mean(numeric_only = True)

    return tenaverage

# ５日移動平均を求める関数
def fiveAverage():

    # ５日分の終値をUSD_JPY_RATEから取り出す処理
    fiveaverage = mongodb_read()
    fiveaverage = fiveaverage.close
    fiveaverage = fiveaverage[:-5] # 最新のものが下にあるので下から取り出してる

    # 終値の平均を算出する処理
    fiveaverage = fiveaverage.mean(numeric_only = True)

    return fiveaverage


# 移動平均のトレンド傾きを調べる関数。連続した線形を微分して、＋か－かで上昇傾向か下降傾向か調べる


# def unknown():
#
#     # 指定日の１０日平均と５日平均の差を見る
#
#     # 指定日の１０日平均の傾向（微分切片）
#
#     # 指定日の５日平均の傾向（微分切片）
#
#     # １０日平均と５日平均がどちらが上にきているか
#     #     ５日平均が１０日平均より上にある場合
#     #       さらに価格が５日平均よりうえなら