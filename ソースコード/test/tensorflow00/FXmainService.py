# -*- coding:utf8 -*-

from predictionService import predictionService
from makeStudyData import GetDate,LateDate
from mongodb_read import mongod_read_find_one,mongodb_read
from OandaApi_timerate import OandaTimeRate
from OandaApiConfig import *
import numpy as np
import pymongo
import schedule
import time, datetime
import workdays
import sys
import const


c = sys.modules["const"]

# 毎日更新する処理群
def daily():
    # predictionServiceを更新する処理
    predictionService()

def UpdateJob():

    # 未決済のトレード情報
    OpenTrade = OpenOrder()
    # トレード情報を取得
    TradeData = Trades()
    # トレード履歴のリスト
    TradeLog = HistricalTrade(10)

    # アカウントのデータ更新　以下が入ってる
    # {'accountId': 2412596,        アカウントID
    #  'realizedPl': 0,             実現損益
    #  'marginRate': 0.04,          銘柄の必要証拠金率
    #  'marginUsed': 0,             現在の中点レートを使用して口座の通貨に変換
    #  'openTrades': 0,             未決済トレードの数
    #  'unrealizedPl': 0,           評価損益
    #  'openOrders': 0,             未決済注文の数
    #  'balance': 3000000,          口座残高
    #  'marginAvail': 3000000,
    #  'accountName': 'Primary',    アカウントの名前
    #  'accountCurrency': 'JPY'}    アカウントの国籍
    AccountData = ResponsAccountDetail()

    print("未決済のトレード情報：\n" + OpenTrade)
    print("トレード情報：\n" + TradeData)
    print("トレードの履歴：\n" + TradeLog)
    print("口座の残高：" + AccountData["balance"])
    print("実現損益：" + AccountData["realizedPl"])
    print("評価損益：" + AccountData["unrealizedPl"])

if __name__ == "__main__":

    # 一日に一回決まった時間に処理を開始する処理
    schedule.every().day.at("5:00").do(daily)
    # 30分ごとにする処理
    schedule.every(30).minutes.do(UpdateJob)
    # １分ごとにする処理
    while (True):
        # スケジューラー発動
        schedule.run_pending()
        # 日付をdatatime形式で取得する処理
        CheckTime = LateDate(1)
        # 営業日か判定する処理
        if (workdays.networkdays(CheckTime, CheckTime) == 1):
            Time = CheckTime.strftime('%Y/%m/%d')
            # predictionServceの更新反映処理
            # P_USD_JPY_RATEの中から、値を指定して取得
            P_USD_JPY = mongod_read_find_one(c.PREDICTION_COL, {"time": Time})
            if(P_USD_JPY["time"] != Time):

                # USD_JPY_RATEを呼び出してDataFrame型で変数に格納,新しい日付が下に来るようにソート
                USD_JPY = mongodb_read(c.STUDY_COL)
                USD_JPY = USD_JPY.sort_values(by="time")
                USD_JPY = USD_JPY.reset_index()
                last = len(USD_JPY) - 1  # 最新データの場所のカーソル

                # P_USD_JPYからclose,high,lowの値をそれぞれ変数に格納
                PClose = P_USD_JPY["close"]
                PHigh = P_USD_JPY["high"]
                PLow = P_USD_JPY["low"]
                # USD_JPY_RATEから昨日のCloseの値を取得
                SClose = USD_JPY["close"][last]

                # 売買の基準となるCloseの設定(翌日予想が前日に比べて高いか低いか)
                if (PClose > SClose):
                    Close = PClose
                    # Unit = 1000
                else:
                    Close = SClose
                    # Unit = 100


            # 現在のレートを格納
            Now_Rate = OandaTimeRate()
            print("１分足の値")
            print(Now_Rate)
            # 売買関数

            time.sleep(60)

        else:
            time.sleep(86400)
            continue

