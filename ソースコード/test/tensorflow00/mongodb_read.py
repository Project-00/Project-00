from pymongo import MongoClient
import pymongo
import os
import sys
import pandas as pd
from mongodb_write import getDBCollection
import pprint



def ReaDB(colName):

    # DBの読み込み先を取得する
    collection = getDBCollection(colName)

    db = collection
    cursor = db.find()
    df =pd.DataFrame.from_dict(list(cursor)).astype(object)

    return df

def mongodb_read(colName):

    df = ReaDB(colName)

    del df["_id"]

    df2 = df.ix[:,["time","close","open","high","low","volume","fiveave","tenave","fiftave",'tma5','tma10',
             'tma15','ema5','ema10','ema15','dema5','dema10','dema15',
             'tema5','tema10','tema15','wma5','wma10','wma15','trend',
             'bbands5up','bbands5mid','bbands5low','bbands10up','bbands10mid',
             'bbands10low','bbands15up','bbands15mid','bbands15low',
             'rocp5','rocp10','rocp15','mom5','mom10','mom15','rsi5','rsi10',
             'rsi15','MACD','MACDsig','MACDhist','apo5','apo10','apo15',
             'ppo5','ppo10','ppo15','cmo5','cmo10','cmo15']]

    return df2

def mongod_read_find_one(colName,calm):

    collection = getDBCollection(colName)

    df2 = collection.find_one(calm)

    return df2

# Predictionデータを取るときの関数
def mongodb_read2(colName):

    df = ReaDB(colName)

    del df["_id"]

    df2 = df.ix[:,["time","close","open","high","low","fiveave","tenave","fiftave",
                   "LSTMclose","LSTM2close"]]

    return df2

# DECISIONデータを取るときの関数
def mongodb_read3(colName):

    df = ReaDB(colName)

    del df["_id"]

    df2 = df.ix[:,["time","PPClose","PPLClose","PPL2Close","PFiveClose","PTenClose","PFiftClose"]]

    return df2