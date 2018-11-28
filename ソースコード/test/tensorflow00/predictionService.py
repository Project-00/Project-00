# -*- coding:utf8 -*-

# 上の層はP_USD_JPY_RATEというテーブルに、翌日の計算予測値を追加する機能
# それぞれの要素のモデルの再教育を施す機能

from makePredictionModel import makePredictionModel
import sys
from makeStudyData import GetDate
import numpy as np
import pandas as pd
from mongodb_write import insertCollection
from mongodb_read import mongodb_read
from previousDataOanda import historyData , oneListWriteForMongo
from MovingAverage import ListAverage

# 下の層はオアンダの履歴を遡ってデータを取得し、データを加工、USD_JPY_RATEというテーブルの中へ格納する
import oandapy

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")


# 定数型の文字列を呼び出す(OPEN,CLOSE,HIGH,LOW)が入ってる　例：c.OPEN
c = sys.modules["const"]


response1 = oanda.get_history(instrument="USD_JPY", granularity="D", count=1)
USD_JPY_D1 = response1.get("candles")

time = USD_JPY_D1[0].get("time")[0:10].replace('-', '/')
# weekday = datetime.strptime(time.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

# 登録の重複を防ぐための措置
check = mongodb_read(c.STUDY_COL)
check = check.sort_values(by="time")
check = check.reset_index()
last = len(check) - 1
# 最新データは最後尾にあるのに注意
if (check["time"][last] != time):
    # USD_JPY_RATEからcloseの中身だけを抽出したあと、新しいcloseを追加（list形式）
    # 空のリスト宣言
    newCloseDataList = []
    for x in check["close"]:
        newCloseDataList.append(x)

    newCloseDataList.append(USD_JPY_D1[0].get("closeBid"))

    # 単純移動平均を作る関数(空のリスト宣言)
    fiveAve = []
    tenAve = []
    fiftAve = []

    five = ListAverage(last+1,5,newCloseDataList)
    ten = ListAverage(last+1,10,newCloseDataList)
    fift = ListAverage(last+1,15,newCloseDataList)

    fiveAve.append(five)
    tenAve.append(ten)
    fiftAve.append(fift)

    result1 = oneListWriteForMongo(USD_JPY_D1,fiveAve,tenAve,fiftAve)

    # # 登録するための辞書作成
    # d = {"time": time, "close": USD_JPY_D1[0].get('closeBid'), 'open': USD_JPY_D1[0].get('openBid'),
    #      'high': USD_JPY_D1[0].get('highBid'), 'low': USD_JPY_D1[0].get('lowBid'),
    #      'volume': USD_JPY_D1[0].get('volume')}
    #
    # result1 = insertCollection("USD_JPY_RATE", d)




# 各値の予測値を取得
P_OPEN = makePredictionModel(c.OPEN)
P_CLOSE = makePredictionModel(c.CLOSE)
P_HIGH = makePredictionModel(c.HIGH)
P_LOW = makePredictionModel(c.LOW)
P_FIVEAVE = makePredictionModel(c.FIVEAVE)
P_TENAVE = makePredictionModel(c.TENAVE)
P_FIFTAVE = makePredictionModel(c.FIFTAVE)

#　時間を取得→実行時間の設定に使うかも？
P_TIME = GetDate()

# 予測値だけを取り出す処理.astype(np.float64)
P_OPEN = P_OPEN[:,0]
P_CLOSE = P_CLOSE[:,0]
P_HIGH = P_HIGH[:,0]
P_LOW = P_LOW[:,0]
P_FIVEAVE = P_FIVEAVE[:,0]
P_TENAVE = P_TENAVE[:,0]
P_FIFTAVE = P_FIFTAVE[:,0]

if (check.iloc[last,0] != time):
    # 辞書キーの作成
    p = {"time": P_TIME, "close": P_CLOSE[0], "open": P_OPEN[0], "high": P_HIGH[0], "low": P_LOW[0],"fiveave": P_FIVEAVE[0],
         "tenave": P_TENAVE[0],"fiftave": P_FIFTAVE[0]
         }

    result1 = insertCollection(c.PREDICTION_COL, p)



