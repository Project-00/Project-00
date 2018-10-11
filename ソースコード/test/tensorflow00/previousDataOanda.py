import oandapy
import pandas as pd
import datetime as dt
from makeStudyData import GetDate
from mongodb_write import insertCollection
import workdays
import const
import sys

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")
# 定数定義呼び出し
c = sys.modules["const"]

# oandaから出てきたリストを加工する関数
def changeListForDict(list):
    d = {"time": list.get('time'), "close": list.get('closeBid'), 'open': list.get('openBid'),
         'high': list.get('highBid'), 'low': list.get('lowBid'),
         'volume': list.get('volume')}

    return d


# parame:年月日（Y M D）が入ってくる
# count:ループ回数
# nowday:月毎や年毎で1日始めで取りたいときに使う。特に指定しない場合は 1 を入力しておく。当日の日付を入力することで1日初めに矯正する。
def historyData(prm,count,nowDay):

    Time = GetDate()
    # 現在の日付を入力した際、0日になるのを回避するため（1日の時等に0日になってしまう）
    Nowday = nowDay - 1
    # 取得した日付からnowDay分引くと1日に矯正できる。矯正しない場合はnowDayに1を入力しておく。
    Time = Time - dt.timedelta(days=Nowday)

    # 初期定義
    endtime = Time
    # count の回数だけ１年ずつ遡って処理する
    # 日取りしたい場合は何日分のデータが欲しいかカウントに代入
    for i in range(count):

        if (prm == c.YEAR):

            # 更新定義(その年によってワークカウントが変わる可能性を考慮)
            # 一年間の範囲を取得
            one_year_ago = endtime - dt.timedelta(year=1)
            workcount = workdays.networkdays(endtime, one_year_ago)

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # weekday = dt.strptime(endtime.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.datetime.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = changeListForDict(USD_JPY_D1)

            # USD_JPY_RATEに格納
            result = insertCollection("USD_JPY_RATE", d)

        elif (prm == c.MONTH):

            one_month_ago = endtime - dt.timedelta(month=1)
            workcount = workdays.networkdays(endtime, one_month_ago)

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.datetime.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = changeListForDict(USD_JPY_D1)

            # USD_JPY_RATEに格納
            result = insertCollection("USD_JPY_RATE", d)


        elif (prm == c.DAY):


            response = oanda.get_history(instrument="USD_JPY", granularity="D", end=endtime, count=1)
            USD_JPY_D1 = response.get("candles")

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.datetime.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = changeListForDict(USD_JPY_D1)

            # USD_JPY_RATEに格納
            result = insertCollection("USD_JPY_RATE", d)


#
# if __name__ == "__main__":
#
#     response1 = oanda.get_history(instrument="USD_JPY", granularity="D", count=5)
#     USD_JPY_D1 = response1.get("candles")
#
#     # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
#     dtime = dt.datetime.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
#     # もう一度RFC3339フォーマットに変換
#     rfc_endtime = dtime.isoformat('T')
#
#     response2 = oanda.get_history(instrument="USD_JPY", granularity="D", end=rfc_endtime, count=5)
#     USD_JPY_D2 = response2.get("candles")
#
#     for d in USD_JPY_D2:
#         print(d)
#     for d in USD_JPY_D1:
#         print(d)

# df = pd.DataFrame(list(USD_JPY_D))
#
# del df["time"]
# del df["complete"]
#
# df.to_csv("sumple_oanda.csv")
#
