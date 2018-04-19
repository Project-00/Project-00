import datetime
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from mongodb_write import getDBCollection
from mongodb_write import insertCollection



# 時間を取る関数
def GetHour():

    #時の取得
    gethour = datetime.now().hour
    #確認出力
    #print(gethour)

    return gethour

# 日にちを取る関数
def GetDate():

    DLT = timezone(timedelta(hours=+0), 'DLT')

    #日にちの取得
    getnow = datetime.now(DLT)

    gettime = getnow.strftime('%Y-%m-%d')
    #確認出力
    #print(gettime)

    return gettime


def GetDocSingleData(clmData,docKey,ad):

    #時刻呼び出し
    nowhour = GetHour()
    nowDate = GetDate()

    # データベースの呼び出し
    client = MongoClient("localhost", 27017)

    mongo_client = MongoClient('localhost:27017')
    db_connect = mongo_client["test_database"]

    # データを取得する
    #始値
    docData = db_connect["TIMERATE"].find({"time":{"$regex": nowDate}}).sort(docKey ,ad).limit(1)

    for data in docData:
        result = data[clmData]

    return result





def insertStudyData():

    #日付
    nowDate = GetDate()
    #始値
    startValue = GetDocSingleData("ask","time",-1)
    # 高値
    highValue = GetDocSingleData("ask","ask",-1)
    # 安値
    lowValue = GetDocSingleData("ask","ask",1)
    # 終値
    endValue = GetDocSingleData("ask", "time", 1)

    #それぞれの値を格納
    point = {
        "DATE": nowDate,
        "STARTVALUE": startValue,
        "HIGHVALUE":highValue,
        "LOWVALUE":lowValue,
        "ENDVALUE":endValue
    }

    #studypointというDBにpointのデータを格納する
    result = insertCollection("STUDYPOINT", point)
    return True