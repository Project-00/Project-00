# -*- coding: utf8 -*-

import numpy as np
from FxMainService import *
from OandaApiConfig import *
from TechnicalApproach import *
from sklearn.linear_model import LinearRegression
import sys
import const
c = sys.modules["const"]
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
config.sections()

# オアンダ講座のアカウント情報

account_id = int(config["OANDA"]["account_id"])
api_key = config["OANDA"]["api_key"]
# アカウントのデータ更新　以下が入ってる
# {'accountId': 2412596,        アカウントID
#  'realizedPl': 0,             実現損益
#  'marginRate': 0.04,          銘柄の必要証拠金率
#  'marginUsed': 0,             現在の中点レートを使用して口座の通貨に変換
#  'openTrades': 0,             未決済トレードの数
#  'unrealizedPl': 0,           評価損益
#  'openOrders': 0,             未決済注文の数
#  'balance': 3000000,          口座残高
#  'marginAvail': 3000000,
#  'accountName': 'Primary',    アカウントの名前
#  'accountCurrency': 'JPY'}    アカウントの国籍
AccountData = ResponsAccountDetail(c.DEMO)
Balance = AccountData["balance"] # 残高