import makeStudyData
import datetime
from datetime import datetime, timedelta, timezone
import csv
from mongodb_write import getDBCollection
from mongodb_write import formatToInsert
from mongodb_write import insertCollection
import pandas as pd

df = pd.read_csv("./__csv__/usd_jpy_api.csv")
colName = 'USD_JPY_RATE'

# DBの書き込み先を取得する
collection = getDBCollection(colName)

#曜日データを格納する関数
def GetDayoftheweek(dt):
    tdatetime = datetime.strptime(dt.replace('/', '-'), '%Y-%m-%d %H:%M:%S')
    DLT = timezone(timedelta(hours=+0), 'DLT')
    #曜日データ取得
    Dotw = tdatetime(DLT)
    getDotw = Dotw.weekday()

    return getDotw


for index, row in df.iterrows():
    # 曜日を取得して格納
    # weekDay = GetDayoftheweek(row.time)
    weekDay = datetime.strptime(row.time.replace('/', '-'), '%Y-%m-%d %H:%M:%S').weekday()
    row['weekday'] = weekDay

    # print(type(index))
    # print(index)
    # print('~~~~~~')
    #
    # print(type(row))
    # print(row)
    # print('------')


    result = insertCollection(colName, row)

    # # コレクションにレコードを書き込みます
    # collection.insert(formatToInsert("time",row.time))
    # collection.insert(formatToInsert("close",row.close))
    # collection.insert(formatToInsert("open",row.open))
    # collection.insert(formatToInsert("high",row.high))
    # collection.insert(formatToInsert("low",row.low))
    # collection.insert(formatToInsert("volume",row.volume))
    # collection.insert(formatToInsert("weekday",row.weekday))

