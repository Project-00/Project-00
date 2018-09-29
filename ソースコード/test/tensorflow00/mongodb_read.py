from pymongo import MongoClient
import pymongo
import os
import sys
import pandas as pd
from mongodb_write import getDBCollection



def ReaDB(collectionName):

    # DBの読み込み先を取得する
    collection = getDBCollection(colName)

    db = collection
    cursor = db.find()
    df =pd.DataFrame.from_dict(list(cursor)).astype(object)

    return df

if __name__ == "__main__":

    # DB(collection)の名前
    colName = 'USD_JPY_RATE'

    df = ReaDB(colName)

    print(df)