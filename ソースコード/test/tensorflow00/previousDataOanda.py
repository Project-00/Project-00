import oandapy
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from makeStudyData import LateDate
from mongodb_write import insertCollection
import workdays
import const
import sys

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")
# 定数定義呼び出し
c = sys.modules["const"]

# oandaから出てきたリストを加工する関数
def ListWriteForMongo(list,workcount):
    for j in range(workcount):

        d = {"time": list[j].get('time'), "close": list[j].get('closeBid'), 'open': list[j].get('openBid'),
             'high': list[j].get('highBid'), 'low': list[j].get('lowBid'),
             'volume': list[j].get('volume')}

        # USD_JPY_RATEに格納
        result = insertCollection("USD_JPY_RATE", d)

    return result


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
        # countの数だけ年数を遡ってデータを取得する
        for i in range(count):

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = ListWriteForMongo(USD_JPY_D1,workcount)

            # weekday = dt.strptime(endtime.replace('/', '-') + " 06:00:00", '%Y-%m-%d %H:%M:%S').weekday()

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # 取得したdtimeから１年（１２か月）引いて１年前を求める
            one_year_ago = dtime - relativedelta(months=12)
            # dtimeからdtimeの１年前までの期間の営業日を求める
            workcount = workdays.networkdays(one_year_ago, dtime)
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')


    # 年同様の動きをする
    elif (prm == c.MONTH):

        one_month_ago = endtime - relativedelta(months=1)
        workcount = workdays.networkdays(endtime, one_month_ago)

        for i in range(count):

            response = oanda.get_history(instrument = "USD_JPY", granularity = "D",end= endtime, count= workcount)
            USD_JPY_D1 = response.get("candles")

            # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
            d = ListWriteForMongo(USD_JPY_D1,workcount)

            # USD_JPY_RATEに格納
            result = insertCollection("USD_JPY_RATE", d)

            # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
            dtime = dt.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            one_month_ago = dtime - relativedelta(months=1)
            workcount = workdays.networkdays(one_month_ago, dtime)
            # もう一度RFC3339フォーマットに変換
            endtime = dtime.isoformat('T')


    # １日だけ動く(1日分のデータ取得)
    elif (prm == c.DAY):

        response = oanda.get_history(instrument="USD_JPY", granularity="D", end=endtime, count=1)
        USD_JPY_D1 = response.get("candles")

        # list(USD_JPY_D1)をdict型にデータを抜き出し加工する
        d = ListWriteForMongo(USD_JPY_D1,1)

        # USD_JPY_RATEに格納
        result = insertCollection("USD_JPY_RATE", d)


#
if __name__ == "__main__":

    result = historyData(c.YEAR,1,18)

    print(result)