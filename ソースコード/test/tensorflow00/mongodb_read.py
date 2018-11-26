from pymongo import MongoClient
import pymongo
import os
import sys
import pandas as pd
from mongodb_write import getDBCollection

# DB(collection)の名前
colName = 'USD_JPY_RATE'

def ReaDB(collectionName):

    # DBの読み込み先を取得する
    collection = getDBCollection(colName)

    db = collection
    cursor = db.find()
    df =pd.DataFrame.from_dict(list(cursor)).astype(object)

    return df

def mongodb_read():

    df = ReaDB(colName)

    del df["_id"]

    df2 = df.ix[:,["time","close","open","high","low","volume","fiveave","tenave","fiftave"]]

    return df2