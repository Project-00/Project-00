import oandapy
import pandas as pd
import datetime as dt

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")

if __name__ == "__main__":

    response1 = oanda.get_history(instrument="USD_JPY", granularity="D", count=500)
    USD_JPY_D1 = response1.get("candles")

    # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
    dtime = dt.datetime.strptime(USD_JPY_D1[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    # もう一度RFC3339フォーマットに変換
    rfc_endtime = dtime.isoformat('T')

    response2 = oanda.get_history(instrument="USD_JPY", granularity="D", end=rfc_endtime, count=500)
    USD_JPY_D2 = response2.get("candles")

    for d in USD_JPY_D2:
        print(d)
    for d in USD_JPY_D1:
        print(d)

    # df = pd.DataFrame(list(USD_JPY_D))
    #
    # del df["time"]
    # del df["complete"]
    #
    # df.to_csv("sumple_oanda.csv")
    #
