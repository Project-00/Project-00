import oandapy
import time
import pymongo
from pymongo import MongoClient
from mongodb_write import getDBCollection
from mongodb_write import formatToInsert
from mongodb_write import insertCollection

oanda = oandapy.API(environment="practice", access_token="806baeb6718f153657980002fea49c6c-2cf6534cb404c014c63931f73fa3def7")

while(True):
    time.sleep(5)
    response = oanda.get_prices(instruments="USD_JPY")
    prices = response.get("prices")
    asking_price = prices[0].get("ask")

    # DBの書き込み先を取得する
    collection = getDBCollection("test_database")

    result = insertCollection("TIMERATE",prices[0])

    # コレクションにレコードを書き込みます
    # collection.insert(formatToInsert("instrument",prices[0].get("instrument")))
    # collection.insert(formatToInsert("time",prices[0].get("time")))
    # collection.insert(formatToInsert("bid",prices[0].get("bid")))
    # collection.insert(formatToInsert("ask",prices[0].get("ask")))

    print(result)
