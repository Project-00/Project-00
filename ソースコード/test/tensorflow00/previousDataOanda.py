import oandapy
import pandas as pd
import datetime as dt
from makeStudyData import GetDate
from mongodb_write import insertCollection
import workdays

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")


# oandaから出てきたリストを加工する関数
def changeListForDict(list, weekday):
    d = {"time": list[0].get('time'), "close": list[0].get('closeBid'), 'open': list[0].get('openBid'),
         'high': list[0].get('highBid'), 'low': list[0].get('lowBid'),
         'volume': list[0].get('volume'), 'weekday': weekday}

    return d


# parame:年月日（Y M D）が入ってくる
# count:ループ回数
# nowday:月毎や年毎で1日始めで取りたいときに使う。特に指定しない場合は 1 を入力しておく
def historyData(parame,count,nowday):

    Time = GetDate()
    # 現在の日付を入力した際、0日になるのを回避するため
    Nowday = nowday - 1
    Time = Time - dt.timedelta(days=Nowday)

    if parame == "Y":
        # 初期定義
        one_year_ago = Time - dt.timedelta(year=1)
        workcount = workdays.networkdays(Time,one_year_ago)
        endtime = Time
        # count の回数だけ１年ずつ遡って処理する
        for i in range(count):

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            weekday = dt.strptime(endtime.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.datetime.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')
            # 更新定義(その年によってワークカウントが変わる可能性を考慮)
            one_year_ago = endtime - dt.timedelta(year=1)
            workcount = workdays.networkdays(endtime, one_year_ago)

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = changeListForDict(USD_JPY_D1,weekday)

            # USD_JPY_RATEに格納
            result = insertCollection("USD_JPY_RATE", d)






    # for i in range(count):
        # response1 =

#
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
