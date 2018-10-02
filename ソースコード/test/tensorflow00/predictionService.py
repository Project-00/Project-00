# -*- coding:utf8 -*-

# 上の層はP_USD_JPY_RATEというテーブルに、翌日の計算予測値を追加する機能
# それぞれの要素のモデルの再教育を施す機能

from makePredictionModel import makePredictionModel
import const
import sys
from makeStudyData import GetDate
import numpy as np
import datetime
from mongodb_write import insertCollection


# 定数型の文字列を呼び出す(OPEN,CLOSE,HIGH,LOW)が入ってる　例：c.OPEN
c = sys.modules["const"]

# 各値の予測値を取得
OPEN = makePredictionModel(c.OPEN)
CLOSE = makePredictionModel(c.CLOSE)
HIGH = makePredictionModel(c.HIGH)
LOW = makePredictionModel(c.LOW)

#　時間を取得→実行時間の設定に使うかも？
TIME = GetDate()

# 予測値だけを取り出す処理
OPEN = OPEN[:,0].astype(np.float64)
CLOSE = CLOSE[:,0].astype(np.float64)
HIGH = HIGH[:,0].astype(np.float64)
LOW = LOW[:,0].astype(np.float64)

# 辞書キーの作成
d = {"time":TIME, "close":CLOSE[0], "open":OPEN[0], "high":HIGH[0], "low":LOW[0]}

result1 = insertCollection("P_USD_JPY_RATE",d)



# 下の層はオアンダの履歴を遡ってデータを取得し、データを加工、USD_JPY_RATEというテーブルの中へ格納する
import oandapy
import pandas as pd
import datetime as dt

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")

response1 = oanda.get_history(instrument="USD_JPY", granularity="D", count=1)
USD_JPY_D1 = response1.get("candles")


