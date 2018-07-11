
# coding:utf-8
from pymongo import MongoClient


#DBの書き込み先を取得する
def getDBCollection(collectionName):

    # LocalhostのMongoDBに書き込みます


    client = MongoClient("localhost",27017)

    # test_databaseというDBを使います
    db = client.test_database

    #コレクションの作成
    # db.createCollection(collectionName)

    # collectionというコレクションを使います
    collection = db[collectionName]

    return collection

# データを書き込み用に変形する
def formatToInsert(key, Contents):
    # DBの  "キー名"     : "データ"
    return {key: Contents}

def insertCollection(collectionName,post):
    collection = getDBCollection(collectionName)

    # idは自動で一意に振り分けられる
    result = collection.insert_one(post)
    return result

