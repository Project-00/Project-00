import oandapy
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from makeStudyData import LateDate
from mongodb_write import insertCollection
import workdays
from MovingAverage import ListAverage
from TechnicalApproach import *
import const
import sys

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")
# 定数定義呼び出し
c = sys.modules["const"]

# 一日分だけ登録する
def oneListWriteForMongo(time, close, open, high, low, volume, sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15):
    d = {"time": time, "close": close,
         'open': open,
         'high': high, 'low': low,
         'volume': volume, 'fiveave': sma5[-1], 'tenave': sma10[-1], 'fiftave': sma15[-1],'tma5':tma5[-1],'tma10':tma10[-1],
             'tma15':tma15[-1],'ema5':ema5[-1],'ema10':ema10[-1],'ema15':ema15[-1],'dema5':dema5[-1],'dema10':dema10[-1],'dema15':dema15[-1],
             'tema5':tema5[-1],'tema10':tema10[-1],'tema15':tema15[-1],'wma5':wma5[-1],'wma10':wma10[-1],'wma15':wma15[-1],'trend':trendline[-1],
             'bbands5up':bbands5[0][-1],'bbands5mid':bbands5[1][-1],'bbands5low':bbands5[2][-1],'bbands10up':bbands10[0][-1],'bbands10mid':bbands10[1][-1],
             'bbands10low':bbands10[2][-1],'bbands15up':bbands15[0][-1],'bbands15mid':bbands15[1][-1],'bbands15low':bbands15[2][-1],
             'rocp5':rocp5[-1],'rocp10':rocp10[-1],'rocp15':rocp15[-1],'mom5':mom5[-1],'mom10':mom10[-1],'mom15':mom15[-1],'rsi5':rsi5[-1],'rsi10':rsi10[-1],
             'rsi15':rsi15[-1],'MACD':macd[0][-1],'MACDsig':macd[1][-1],'MACDhist':macd[2][-1],'apo5':apo5[-1],'apo10':apo10[-1],'apo15':apo15[-1],
             'ppo5':ppo5[-1],'ppo10':ppo10[-1],'ppo15':ppo15[-1],'cmo5':cmo5[-1],'cmo10':cmo10[-1],'cmo15':cmo15[-1]
         }

    # USD_JPY_RATEに格納
    result = insertCollection(c.STUDY_COL, d)

    return result


# oandaから出てきたリストと移動平均等のリストを一括で登録する関数
def ListWriteForMongo(list,sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15):

    # 15番目からスタートして最後まで（15日平均に合わせる）
    for j in range(100,len(list)):

        d = {"time": list[j].get('time')[:10].replace('-','/'), "close": list[j].get('closeBid'), 'open': list[j].get('openBid'),
             'high': list[j].get('highBid'), 'low': list[j].get('lowBid'),
             'volume': list[j].get('volume'),'fiveave':sma5[j],'tenave':sma10[j],'fiftave':sma15[j],'tma5':tma5[j],'tma10':tma10[j],
             'tma15':tma15[j],'ema5':ema5[j],'ema10':ema10[j],'ema15':ema15[j],'dema5':dema5[j],'dema10':dema10[j],'dema15':dema15[j],
             'tema5':tema5[j],'tema10':tema10[j],'tema15':tema15[j],'wma5':wma5[j],'wma10':wma10[j],'wma15':wma15[j],'trend':trendline[j],
             'bbands5up':bbands5[0][j],'bbands5mid':bbands5[1][j],'bbands5low':bbands5[2][j],'bbands10up':bbands10[0][j],'bbands10mid':bbands10[1][j],
             'bbands10low':bbands10[2][j],'bbands15up':bbands15[0][j],'bbands15mid':bbands15[1][j],'bbands15low':bbands15[2][j],
             'rocp5':rocp5[j],'rocp10':rocp10[j],'rocp15':rocp15[j],'mom5':mom5[j],'mom10':mom10[j],'mom15':mom15[j],'rsi5':rsi5[j],'rsi10':rsi10[j],
             'rsi15':rsi15[j],'MACD':macd[0][j],'MACDsig':macd[1][j],'MACDhist':macd[2][j],'apo5':apo5[j],'apo10':apo10[j],'apo15':apo15[j],
             'ppo5':ppo5[j],'ppo10':ppo10[j],'ppo15':ppo15[j],'cmo5':cmo5[j],'cmo10':cmo10[j],'cmo15':cmo15[j]
             }

        # USD_JPY_RATEに格納
        result = insertCollection(c.STUDY_COL, d)

    return result

# 学習機の正答率の判定結果を登録するための関数
def DecisionWriteForMongo(time,list):
    d = {"time":time,"PPClose":list[0],"PPLClose":list[1],"PPL2Close":list[2],"PFiveClose":list[3],"PTenClose":list[4],"PFiftClose":list[5]}

    insertCollection(c.DECISION_COL, d)
    return


# parame:年月日（Y M D）が入ってくる
# count:ループ回数
# nowDay:月毎や年毎で1日始めで取りたいときに使う。特に指定しない場合は 1 を入力しておく。当日の日付を入力することで1日初めに矯正する。
def historyData(prm,count,nowDay):

    # nowDayに入った数だけ日付を減算することで、１日目からの取得に変えれる。変えない場合はnowDayに１を入れておく。
    Time = LateDate(nowDay)

    # 初期定義
    endtime = Time
    # count の回数だけ１年ずつ遡って処理する
    if (prm == c.YEAR):
        # 初期定義
        # 日取りしたい場合は何日分のデータが欲しいかカウントに代入
        # 更新定義(その年によってワークカウントが変わる可能性を考慮)
        # 一年間の範囲を取得
        one_year_ago = endtime - relativedelta(months=12)
        workcount = workdays.networkdays(one_year_ago, endtime)
        endtime = Time.isoformat('T')

        # 登録データ
        usdJpyDataList = []

        # countの数だけ年数を遡ってデータを取得する
        for i in range(count):

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            # d = ListWriteForMongo(USD_JPY_D1)
            for j in USD_JPY_D1:
                usdJpyDataList.append(j)

            # weekday = dt.strptime(endtime.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # 取得したdtimeから１年（１２か月）引いて１年前を求める
            one_year_ago = dtime - relativedelta(months=12)
            # dtimeからdtimeの１年前までの期間の営業日を求める
            workcount = workdays.networkdays(one_year_ago, dtime)
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')

        # リストを日付順にソートする
        usdJpyDataList.sort(key=lambda x: x['time'])

        # 5日平均、10日平均、15日平均のリストを作成
        # 15日平均に合わせて要素を削除
        Closelist = []
        for w in range(len(usdJpyDataList)):
            Closelist.append(usdJpyDataList[w].get("closeBid"))

        sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15 = AllMakeTechnical(
            Closelist)
        d = ListWriteForMongo(usdJpyDataList,sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15)


    # # 年同様の動きをする
    # elif (prm == c.MONTH):
    #
    #     one_month_ago = endtime - relativedelta(months=1)
    #     workcount = workdays.networkdays(endtime, one_month_ago)
    #
    #     for i in range(count):
    #
    #         response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
    #         USD_JPY_D1 = response.get("candles")
    #
    #         # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
    #         d = ListWriteForMongo(USD_JPY_D1)
    #
    #         # USD_JPY_RATEに格納
    #         result = insertCollection(c.STUDY_COL, d)
    #
    #         # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
    #         dtime = dt.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #         one_month_ago = dtime - relativedelta(months=1)
    #         workcount = workdays.networkdays(one_month_ago, dtime)
    #         # もう一度RFC3339フォーマットに変換
    #         endtime = dtime.isoformat('T')


    # １日だけ動く(1日分のデータ取得)
    elif (prm == c.DAY):

        response = oanda.get_history(instrument="USD_JPY", granularity="D", end=endtime, count=1)
        USD_JPY_D1 = response.get("candles")

        # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
        d = ListWriteForMongo(USD_JPY_D1)

        # USD_JPY_RATEに格納
        result = insertCollection(c.STUDY_COL, d)


#
# if __name__ == "__main__":
#
#     # 引数は　年月日コード　取りたい年数分　当日以前ならば１、月の頭（１日）からなら現在日付けを入力
#     result = historyData(c.YEAR,20,1)
#
#     print("終わりました")