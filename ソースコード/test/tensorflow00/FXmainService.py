# -*- coding:utf8 -*-

from predictionService import predictionService
from makeStudyData import GetDate,LateDate,GetHour
from mongodb_read import *
from OandaApi_timerate import OandaTimeRate
from OandaApiConfig import *
from TechnicalApproach import *
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from previousDataOanda import *
import numpy as np
import pymongo
import schedule
import time, datetime
import workdays
import sys
import const
import oandapy

api_key = config["OANDA"]["api_key"]
oanda = oandapy.API(environment="practice", access_token= api_key)

c = sys.modules["const"]
act = True


def ini():
    act = True
    USD_JPY = mongodb_read(c.STUDY_COL)
    USD_JPY = USD_JPY.sort_values(by="time")
    USD_JPY = USD_JPY.reset_index()
    last_1 = len(USD_JPY) - 1
    P_USD_JPY = mongodb_read2(c.PREDICTION_COL)
    P_USD_JPY = P_USD_JPY.sort_values(by="time")
    P_USD_JPY = P_USD_JPY.reset_index()
    last_2 = len(P_USD_JPY) - 1

    # P_USD_JPYからclose,high,lowの値をそれぞれ変数に格納
    PClose = P_USD_JPY["close"][last_2]
    PLClose = P_USD_JPY["LSTMclose"][last_2]
    PL2Close = P_USD_JPY["LSTM2close"][last_2]
    # PHigh = P_USD_JPY["high"][last_2]
    # PLow = P_USD_JPY["low"][last_2]
    PFive = P_USD_JPY["fiveave"][last_2]
    PTen = P_USD_JPY["tenave"][last_2]
    PFift = P_USD_JPY["fiftave"][last_2]
    # USD_JPY_RATEから昨日のCloseの値を取得
    SClose = USD_JPY["close"][last_1]
    # 予測した移動平均から実際の値を引いて出したCloseの値（参考用）
    FiveClose = (5 * PFive) - sum(USD_JPY["close"][len(USD_JPY) - 4:])
    TenClose = (10 * PTen) - sum(USD_JPY["close"][len(USD_JPY) - 9:])
    FiftClose = (15 * PFift) - sum(USD_JPY["close"][len(USD_JPY) - 14:])

    # DECI(判定結果)から精度を更新
    DECI = mongodb_read3(c.DECISION_COL)
    DECI = DECI.sort_values(by="time")
    DECI = DECI.reset_index()
    U = len(DECI)
    # 正解した数/試行数で正答精度を調べる
    probPClose = sum(DECI["PPClose"]) / U
    probPLClose = sum(DECI["PPLClose"]) / U
    probPL2Close = sum(DECI["PPL2Close"]) / U
    probFiveClose = sum(DECI["PFiveClose"]) / U
    probTenClose = sum(DECI["PTenClose"]) / U
    probFiftClose = sum(DECI["PFiftClose"]) / U

    return act,PClose,PLClose,PL2Close,PFive,PTen,PFift,SClose,FiveClose,TenClose,FiftClose\
        ,probPClose,probPLClose,probPL2Close,probFiveClose,probTenClose,probFiftClose


# 学習機の信頼性を評価と保存をするための関数(それぞれの予測値をまとめて引数に持ってくる)
def PredictionScore(PClose,PLClose,PL2Close,FiveClose,TenClose,FiftClose):

    # 改変の際は予測値の順序だけ要注意！
    Plist = [PClose,PLClose,PL2Close,FiveClose,TenClose,FiftClose]

    USD_JPY = mongodb_read(c.STUDY_COL)
    USD_JPY = USD_JPY.sort_values(by="time")
    USD_JPY = USD_JPY.reset_index()
    last = len(USD_JPY) - 1

    # 前日と比較して上がったのか下がったのか結果を調べる
    # USD_JPYから比較用のCloseのデータを取ってくる
    Close1 = USD_JPY["close"][last]         # 最新のデータ
    Close2 = USD_JPY["close"][last - 1]     # 最新の一つ前のデータ
    delta = Close1 - Close2                  # 実際のClose値で前日と比べて上がったか下がったか調べるもの
    delta2 = [i - Close2 for i in Plist]    # Closeから予測値を引いた値のリスト
    Decision = []                            # 判定結果を入れるリスト
    # 判定(正又は同値なら１、負なら０)
    if delta >= 0:
        for i in delta2:
            if i >= 0:
                Decision.append(1)
            else:
                Decision.append(0)
    else:
        for i in delta2:
            if i <= 0:
                Decision.append(1)
            else:
                Decision.append(0)

    time = GetDate()

    DecisionWriteForMongo(time,Decision)

    return print("評価値の保存完了")


def UpdateJob():

    # 未決済のトレード情報
    OpenTrade = OpenOrder(c.DEMO)
    # トレード情報を取得
    TradeData = Trades(c.DEMO)
    # トレード履歴のリスト
    TradeLog = HistricalTrade(c.DEMO,10)

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
    AccountData = ResponsAccountDetail(c.DEMO)

    print("未決済のトレード情報：")
    print(OpenTrade)
    print("トレード情報：")
    print(TradeData)
    print("トレードの履歴：")
    print(TradeLog)
    print("口座の残高：")
    print(AccountData["balance"])
    print("実現損益：")
    print(AccountData["realizedPl"])
    print("評価損益：")
    print(AccountData["unrealizedPl"])
    return


def oneDatamake(key):
    result = False

    checkhour = GetHour()

    if((key == True) and (checkhour >= 21)):
        # 登録の重複を防ぐための措置
        check = mongodb_read(c.STUDY_COL)
        check = check.sort_values(by="time")
        check = check.reset_index()
        last = len(check) - 1

        time = GetDate()
        # 夜中に更新すると翌日の予想なのに日付がずれるので修正
        time = dt.strptime(time, '%Y/%m/%d')
        time = time + timedelta(days=1)
        time = time.strftime('%Y/%m/%d')

        # 最新データは最後尾にあるのに注意
        if (check["time"][last] != time):

            usdJpyDataList = []
            Date = dt.now()
            # OpenDate = dt(Date.year,Date.month,Date.day,7,0,0,0)
            CloseDate = dt(Date.year,Date.month,Date.day,21,0,0,0)
            # opentime = OpenDate.isoformat('T')
            closetime = CloseDate.isoformat('T')

            endtime = closetime

            # 5秒足の1日分のデータ(10秒感覚のを0~21時分)をループを使って取っていく
            for i in range(2):
                response = oanda.get_history(instrument="USD_JPY", granularity="S10", end=endtime, count=2680)
                USD_JPY_S10 = response.get("candles")

                # # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
                # d = ListWriteForMongo(USD_JPY_D1)
                for j in USD_JPY_S10:
                    usdJpyDataList.append(j)

                # weekday = dt.strptime(endtime.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

                # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
                dtime = dt.strptime(USD_JPY_S10[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')

                # もう一度RFC3339フォーマットに変換
                endtime = dtime.isoformat('T')

            # リストを時間順にソートする
            usdJpyDataList.sort(key=lambda x: x['time'])
            del usdJpyDataList[0]

            HighList = []
            LowList = []
            volumeList = []

            for x in range(len(usdJpyDataList)):
                HighList.append(usdJpyDataList[x]['highBid'])
                LowList.append(usdJpyDataList[x]['lowBid'])
                volumeList.append(usdJpyDataList[x]['volume'])

            Open = usdJpyDataList[0]['openBid']
            Close = usdJpyDataList[-1]['closeBid']
            High = max(HighList)
            Low = min(LowList)
            Volume = sum(volumeList)

            # モンゴからcloseのデータセットを取得

            Data = mongodb_read(c.STUDY_COL)
            Data = Data.sort_values(by="time")
            Data = Data.reset_index()

            newCloseDataList = []
            for x in Data["close"]:
                newCloseDataList.append(x)

            newCloseDataList.append(Close)
            newCloseDataList = changelist1(newCloseDataList)

            sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15 = AllMakeTechnical(
                newCloseDataList)

            d = oneListWriteForMongo(time,Close,Open,High,Low,Volume,sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15)

            print("学習用のデータベースの更新完了")
            result = True

    return result


if __name__ == "__main__":

    # 30分ごとにする処理
    schedule.every(30).minutes.do(UpdateJob)

    # 初期化値
    act, PClose, PLClose, PL2Close, PFive, PTen, PFift, SClose, FiveClose, TenClose, FiftClose\
        , probPClose, probPLClose, probPL2Close, probFiveClose, probTenClose, probFiftClose = ini()

    while(True):

        # 日付をdatatime形式で取得する処理
        CheckTime = LateDate(1)
        CheckTime = CheckTime + timedelta(days=1)
        # 学習用データを更新する処理
        update = oneDatamake(act)

        # 翌日が営業日か判定する処理
        if (workdays.networkdays(CheckTime, CheckTime) >= 1):
            Time = CheckTime.strftime('%Y/%m/%d')
            # predictionServiceのデータベース更新の確認が取れたら起動
            if (update == True):
                PredictionScore(PClose,PLClose,PL2Close,FiveClose,TenClose,FiftClose)
                preresult = predictionService()
                # P_USD_JPY_RATEの中から、値を指定して取得
                P_USD_JPY = mongod_read_find_one(c.PREDICTION_COL, {"time": Time})

                # USD_JPY_RATEを呼び出してDataFrame型で変数に格納,新しい日付が下に来るようにソート
                USD_JPY = mongodb_read(c.STUDY_COL)
                USD_JPY = USD_JPY.sort_values(by="time")
                USD_JPY = USD_JPY.reset_index()

                # P_USD_JPYからclose,high,lowの値をそれぞれ変数に格納
                PClose = P_USD_JPY["close"]
                PLClose = P_USD_JPY["LSTMclose"]
                PL2Close = P_USD_JPY["LSTM2close"]
                # PHigh = P_USD_JPY["high"]
                # PLow = P_USD_JPY["low"]
                PFive = P_USD_JPY["fiveave"]
                PTen = P_USD_JPY["tenave"]
                PFift = P_USD_JPY["fiftave"]
                # USD_JPY_RATEから昨日のCloseの値を取得
                SClose = USD_JPY["close"][len(USD_JPY)-1]
                # 予測した移動平均から実際の値を引いて出したCloseの値（参考用）
                FiveClose = (5 * PFive) - sum(USD_JPY["close"][len(USD_JPY)-4:])
                TenClose = (10 * PTen) - sum(USD_JPY["close"][len(USD_JPY)-9:])
                FiftClose = (15 * PFift) - sum(USD_JPY["close"][len(USD_JPY)-14:])

                # DECI(判定結果)から精度(確率)を更新
                DECI = mongodb_read3(c.DECISION_COL)
                DECI = DECI.sort_values(by="time")
                DECI = DECI.reset_index()
                U = len(DECI)
                # 正解した数/試行数で正答精度を調べる
                probPClose = sum(DECI["PPClose"]) / U
                probPLClose = sum(DECI["PPLClose"]) / U
                probPL2Close = sum(DECI["PPL2Close"]) / U
                probFiveClose = sum(DECI["PFiveClose"]) / U
                probTenClose = sum(DECI["PTenClose"]) / U
                probFiftClose = sum(DECI["PFiftClose"]) / U

        hour = GetHour()
        # 活動時間範囲を決める処理
        # 終了時間判定(AM７時以下の時、21:00～6:59時の間になるとオペレーション終了)
        if (hour < 7 or hour >= 21):

            if((act == False) and (update == False)):
                act = True

            # 1分置きにチェックさせる
            time.sleep(60)
        else:
            # スケジューラー発動
            schedule.run_pending()
            # １分ごとにする処理
            # 現在のレートを格納
            Now_Rate = OandaTimeRate()
            print("１分足の値")
            print(Now_Rate)
            # 売買関数

            act = False
            time.sleep(60)

