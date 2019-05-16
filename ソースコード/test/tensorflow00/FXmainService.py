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
from collections import deque
from TradeSignal import *
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
AccountData = ResponsAccountDetail(c.DEMO)

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

    # DECI(判定結果)から精度(確率)を更新
    # 流動性を持たせるために最新100件の間にすること
    # 暫定的な処理なので注意（汎用性を持たせるとすれば、各カラムごとにループを使って計算すること）
    DECI = mongodb_read3(c.DECISION_COL)
    DECI = DECI.sort_values(by="time")
    DECI = DECI.reset_index()
    # それぞれの母数を求める処理
    PCU = len(DECI["PPClose"])  # PClose
    PLCU = len(DECI["PPLClose"])  # PLClose
    PL2CU = len(DECI["PPL2Close"])  # PL2Close
    PFVCU = len(DECI["PFiveClose"])  # PFiveClose
    PTCU = len(DECI["PTenClose"])  # PTenClose
    PFFCU = len(DECI["PFiftClose"])  # PFiftClose

    # 正解した数/試行数で正答精度を調べる(個別に反映させられるようにすること)
    if PCU < 100:
        probPClose = sum(DECI["PPClose"]) / PCU
    else:
        probPClose = sum(DECI["PPClose"][len(DECI) - 100:]) / 100
    if PLCU < 100:
        probPLClose = sum(DECI["PPLClose"]) / PLCU
    else:
        probPLClose = sum(DECI["PPLClose"][len(DECI) - 100:]) / 100
    if PL2CU < 100:
        probPL2Close = sum(DECI["PPL2Close"]) / PL2CU
    else:
        probPL2Close = sum(DECI["PPL2Close"][len(DECI) - 100:]) / 100
    if PFVCU < 100:
        probFiveClose = sum(DECI["PFiveClose"]) / PFVCU
    else:
        probFiveClose = sum(DECI["PFiveClose"][len(DECI) - 100:]) / 100
    if PTCU < 100:
        probTenClose = sum(DECI["PTenClose"]) / PTCU
    else:
        probTenClose = sum(DECI["PTenClose"][len(DECI) - 100:]) / 100
    if PFFCU < 100:
        probFiftClose = sum(DECI["PFiftClose"]) / PFFCU
    else:
        probFiftClose = sum(DECI["PFiftClose"][len(DECI) - 100:]) / 100

    # 先日のCloseと大小を図って確率を加算していく
    # 確率の多数決のための処理
    # 初期化
    AboveScore = 0.0  # 以上
    BelowScore = 0.0  # 以下
    Asumc = 0.0  # 以上に分類されたCloseを加算
    Bsumc = 0.0  # 以下に分類されたCloseを加算
    An = 0.0  # 以上に分類された数
    Bn = 0.0  # 以下に分類された数

    if SClose <= PClose:
        AboveScore += probPClose
        Asumc += PClose
        An += 1.0
    else:
        BelowScore += probPClose
        Bsumc += PClose
        Bn += 1.0

    if SClose <= PLClose:
        AboveScore += probPLClose
        Asumc += PLClose
        An += 1.0
    else:
        BelowScore += probPLClose
        Bsumc += PLClose
        Bn += 1.0

    if SClose <= PL2Close:
        AboveScore += probPL2Close
        Asumc += PL2Close
        An += 1.0
    else:
        BelowScore += probPL2Close
        Bsumc += PL2Close
        Bn += 1.0

    if SClose <= FiveClose:
        AboveScore += probFiveClose
        Asumc += FiveClose
        An += 1.0
    else:
        BelowScore += probFiveClose
        Bsumc += FiveClose
        Bn += 1.0

    if SClose <= TenClose:
        AboveScore += probTenClose
        Asumc += TenClose
        An += 1.0
    else:
        BelowScore += probTenClose
        Bsumc += TenClose
        Bn += 1.0

    if SClose <= FiftClose:
        AboveScore += probFiftClose
        Asumc += FiftClose
        An += 1.0
    else:
        BelowScore += probFiftClose
        Bsumc += FiftClose
        Bn += 1.0

    # 算出したaboveとbelowを使ってユニット量を決めておく
    # 残高の割合で決める
    # 仮に資本金３０万ならば、現在の値段×Unit量で取引限界を考える
    # 下記のような条件ならば、現在値を120と仮定すると１回取引辺り36000円動く形になる
    # Unitが100以下になる（残高10万を下回る）と取引できないかもしれない？
    if AboveScore > BelowScore:  # 前日より上がると予想した時、強気の勝負
        if AccountData["balance"] > 100000:
            # Unit = AccountData["balance"] / 1000
            Unit = 10000
        else:
            Unit = 10000
        # 前日より上がると予想したCloseの平均値
        StandardClose = (Asumc / An)
    else:  # 前日より下がると予想した時、消極的勝負
        if AccountData["balance"] > 100000:
            # Unit = AccountData["balance"] / 2000
            Unit = 10000
        else:
            Unit = 10000
        # 前日より下がると予想したCloseの平均値
        StandardClose = (Bsumc / Bn)

    return act,PClose,PLClose,PL2Close,PFive,PTen,PFift,SClose,FiveClose,TenClose,FiftClose\
        ,probPClose,probPLClose,probPL2Close,probFiveClose,probTenClose,probFiftClose\
        ,Unit,StandardClose


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

    if((key == True) and ((checkhour >= 21) or (checkhour <= 1))):
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

            # 0時過ぎてしまった時の緊急用措置軍
            if(checkhour <=7):
                Date = Date - timedelta(days = 1)
                time = dt.strptime(time, '%Y/%m/%d')
                time = time - timedelta(days=1)
                time = time.strftime('%Y/%m/%d')

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
        , probPClose, probPLClose, probPL2Close, probFiveClose, probTenClose, probFiftClose\
        ,Unit,StandardClose = ini()

    # 値をＮ個格納するキューのリスト
    queue = deque()

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
            # １日の方針情報の更新
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
                # 流動性を持たせるために最新100件の間にすること
                # 暫定的な処理なので注意（汎用性を持たせるとすれば、各カラムごとにループを使って計算すること）
                DECI = mongodb_read3(c.DECISION_COL)
                DECI = DECI.sort_values(by="time")
                DECI = DECI.reset_index()
                # それぞれの母数を求める処理
                PCU = len(DECI["PPClose"])          # PClose
                PLCU = len(DECI["PPLClose"])        # PLClose
                PL2CU = len(DECI["PPL2Close"])      # PL2Close
                PFVCU = len(DECI["PFiveClose"])     # PFiveClose
                PTCU = len(DECI["PTenClose"])       # PTenClose
                PFFCU = len(DECI["PFiftClose"])     # PFiftClose

                # 正解した数/試行数で正答精度を調べる(個別に反映させられるようにすること)
                if PCU < 100:
                    probPClose = sum(DECI["PPClose"]) / PCU
                else:
                    probPClose = sum(DECI["PPClose"][len(DECI) - 100:]) / 100
                if PLCU < 100:
                    probPLClose = sum(DECI["PPLClose"]) / PLCU
                else:
                    probPLClose = sum(DECI["PPLClose"][len(DECI)-100:]) / 100
                if PL2CU < 100:
                    probPL2Close = sum(DECI["PPL2Close"]) / PL2CU
                else:
                    probPL2Close = sum(DECI["PPL2Close"][len(DECI)-100:]) / 100
                if PFVCU < 100:
                    probFiveClose = sum(DECI["PFiveClose"]) / PFVCU
                else:
                    probFiveClose = sum(DECI["PFiveClose"][len(DECI)-100:]) / 100
                if PTCU < 100:
                    probTenClose = sum(DECI["PTenClose"]) / PTCU
                else:
                    probTenClose = sum(DECI["PTenClose"][len(DECI)-100:]) / 100
                if PFFCU < 100:
                    probFiftClose = sum(DECI["PFiftClose"]) / PFFCU
                else:
                    probFiftClose = sum(DECI["PFiftClose"][len(DECI)-100:]) / 100

                # 先日のCloseと大小を図って確率を加算していく
                # 確率の多数決のための処理
                # 初期化
                AboveScore = 0.0     # 以上
                BelowScore = 0.0     # 以下
                Asumc = 0.0          # 以上に分類されたCloseを加算
                Bsumc = 0.0          # 以下に分類されたCloseを加算
                An = 0.0             # 以上に分類された数
                Bn = 0.0             # 以下に分類された数

                if SClose <= PClose:
                    AboveScore += probPClose
                    Asumc += PClose
                    An += 1.0
                else:
                    BelowScore += probPClose
                    Bsumc += PClose
                    Bn += 1.0

                if SClose <= PLClose:
                    AboveScore += probPLClose
                    Asumc += PLClose
                    An += 1.0
                else:
                    BelowScore += probPLClose
                    Bsumc += PLClose
                    Bn += 1.0

                if SClose <= PL2Close:
                    AboveScore += probPL2Close
                    Asumc += PL2Close
                    An += 1.0
                else:
                    BelowScore += probPL2Close
                    Bsumc += PL2Close
                    Bn += 1.0

                if SClose <= FiveClose:
                    AboveScore += probFiveClose
                    Asumc += FiveClose
                    An += 1.0
                else:
                    BelowScore += probFiveClose
                    Bsumc += FiveClose
                    Bn += 1.0

                if SClose <= TenClose:
                    AboveScore += probTenClose
                    Asumc += TenClose
                    An += 1.0
                else:
                    BelowScore += probTenClose
                    Bsumc += TenClose
                    Bn += 1.0

                if SClose <= FiftClose:
                    AboveScore += probFiftClose
                    Asumc += FiftClose
                    An += 1.0
                else:
                    BelowScore += probFiftClose
                    Bsumc += FiftClose
                    Bn += 1.0

                # 算出したaboveとbelowを使ってユニット量を決めておく
                # 残高の割合で決める
                # 仮に資本金３０万ならば、現在の値段×Unit量で取引限界を考える
                # 下記のような条件ならば、現在値を120と仮定すると１回取引辺り36000円動く形になる
                # デモ口座だと最低通貨量が10000らしい……　プロ口座は1000なのでもう少し細かくできる
                if AboveScore > BelowScore:       # 前日より上がると予想した時、強気の勝負
                    if AccountData["balance"] > 100000:
                        # Unit = AccountData["balance"] / 10000
                        Unit = 10000
                    else:
                        Unit = 10000
                    # 前日より上がると予想したCloseの平均値
                    StandardClose = (Asumc / An)
                else:                   # 前日より下がると予想した時、消極的勝負
                    if AccountData["balance"] > 100000:
                        # Unit = AccountData["balance"] / 2000
                        Unit = 10000
                    else:
                        Unit = 10000
                    # 前日より下がると予想したCloseの平均値
                    StandardClose = (Bsumc / Bn)


        hour = GetHour()
        # 活動時間範囲を決める処理
        # 終了時間判定(AM７時以下の時、21:00～6:59時の間になるとオペレーション終了)
        if (hour < 7 or hour >= 21):

            if((act == False) and (update == False)):
                act = True

            # 1分置きにチェックさせる
            time.sleep(600)
        else:
            # スケジューラー発動
            schedule.run_pending()
            # １分ごとにする処理
            # 現在のレートを格納
            Now_Rate = OandaTimeRate()
            # キューの中に格納（720個を超えた場合は古い物から捨てる）
            if len(queue) > 720:
                queue.append([Now_Rate])
                queue.popleft()
            else:
                queue.append([Now_Rate])

            print("現時点の値")
            print(Now_Rate)
            # 売買関数
            # トレンド推移状況を見るためのqueueが十分にそろってから動くようにする
            if len(queue) >60:
                O = TradeOrder(Now_Rate,queue,Unit,StandardClose)

            act = False
            time.sleep(10)

