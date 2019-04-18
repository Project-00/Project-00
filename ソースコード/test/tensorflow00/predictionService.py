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
from datetime import datetime as dt
from datetime import timedelta
from TechnicalApproach import *
from LSTMTensor import *
from LSTMTensor2 import *
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
config.sections()

# 下の層はオアンダの履歴を遡ってデータを取得し、データを加工、USD_JPY_RATEというテーブルの中へ格納する
import oandapy

api_key = config["OANDA"]["api_key"]
oanda = oandapy.API(environment="practice", access_token= api_key)


# 定数型の文字列を呼び出す(OPEN,CLOSE,HIGH,LOW)が入ってる　例：c.OPEN
c = sys.modules["const"]

def predictionService():

    result = False
    # response1 = oanda.get_history(instrument="USD_JPY", granularity="D", count=1)
    # USD_JPY_D1 = response1.get("candles")
    #
    # time = GetDate()
    # # weekday = datetime.strptime(time.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()
    #
    # # 登録の重複を防ぐための措置
    # check = mongodb_read(c.STUDY_COL)
    # check = check.sort_values(by="time")
    # check = check.reset_index()
    # last = len(check) - 1
    # # 最新データは最後尾にあるのに注意
    # if (check["time"][last] != time):
    #     # USD_JPY_RATEからcloseの中身だけを抽出したあと、新しいcloseを追加（list形式）
    #     # 空のリスト宣言
    #     newCloseDataList = []
    #     for x in check["close"]:
    #         newCloseDataList.append(x)
    #
    #     newCloseDataList.append(USD_JPY_D1[0].get("closeBid"))
    #
    #     newCloseDataList = changelist1(newCloseDataList)
    #
    #     sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15 = AllMakeTechnical(
    #         newCloseDataList)
    #     d = oneListWriteForMongo(time,USD_JPY_D1[0]['closeBid'],USD_JPY_D1[0]['openBid'],USD_JPY_D1[0]['highBid'],USD_JPY_D1[0]['lowBid'],USD_JPY_D1[0]['volume'],
    #                              sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15)
    #
    #
    #     print(time + "分のデータ更新と登録完了")
    #
    #

    #　時間を取得→実行時間の設定に使うかも？
    P_TIME = GetDate()
    P_TIME = dt.strptime(P_TIME, '%Y/%m/%d')
    P_TIME = P_TIME + timedelta(days=1)
    P_TIME = P_TIME.strftime('%Y/%m/%d')

    # 各値の予測値を取得
    # P_OPEN = makePredictionModel(c.OPEN)
    P_CLOSE = makePredictionModel(c.CLOSE)
    # P_HIGH = makePredictionModel(c.HIGH)
    # P_LOW = makePredictionModel(c.LOW)
    P_FIVEAVE = makePredictionModel(c.FIVEAVE)
    P_TENAVE = makePredictionModel(c.TENAVE)
    P_FIFTAVE = makePredictionModel(c.FIFTAVE)


    # 予測値だけを取り出す処理.astype(np.float64)
    # P_OPEN = P_OPEN[:,0]
    P_CLOSE = P_CLOSE[:,0]
    # P_HIGH = P_HIGH[:,0]
    # P_LOW = P_LOW[:,0]
    P_FIVEAVE = P_FIVEAVE[:,0]
    P_TENAVE = P_TENAVE[:,0]
    P_FIFTAVE = P_FIFTAVE[:,0]
    P_L_CLOSE = LSTMprediction()
    P_L2_CLOSE = LSTM2prediction()

    # if (check.iloc[-1,0] != time):
    #     # 辞書キーの作成
    #     p = {"time": P_TIME, "close": P_CLOSE[0],"fiveave": P_FIVEAVE[0],
    #          "tenave": P_TENAVE[0],"fiftave": P_FIFTAVE[0],"LSTMclose":P_L_CLOSE,"LSTM2close":P_L2_CLOSE
    #          }
    #
    #     result1 = insertCollection(c.PREDICTION_COL, p)
    #
    #     print(P_TIME + "分の予測データの登録完了")

    p = {"time": P_TIME, "close": P_CLOSE[0], "fiveave": P_FIVEAVE[0],
         "tenave": P_TENAVE[0], "fiftave": P_FIFTAVE[0], "LSTMclose": P_L_CLOSE, "LSTM2close": P_L2_CLOSE
         }

    result1 = insertCollection(c.PREDICTION_COL, p)

    print(P_TIME + "分の予測データの登録完了")

    print("予測データベースの更新処理完了")


    return result

if __name__ == "__main__":
    predictionService()