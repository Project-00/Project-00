# -*- coding: utf-8 -*-

import oandapy
import pandas as pd
import sys
import const
# 定数型の文字列を呼び出す(OPEN,CLOSE,HIGH,LOW)が入ってる　例：c.OPEN
c = sys.modules["const"]
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
config.sections()

# チュートリアル講座のアカウント情報

account_id = int(config["OANDA"]["account_id"])
api_key = config["OANDA"]["api_key"]


# ----------トレードの管理系関数群--------------

# 口座の詳細情報を取得する関数
def ResponsAccountDetail(prm):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    res_acct_detail = oanda.get_account(account_id= account_id)
    # balance: 口座残高
    # realizedPI: 実現損益
    # unrealizedPI: 評価損益
    return res_acct_detail

# オープントレードを取得(未決済のトレード表示)
def OpenOrder(prm):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    open_orders = oanda.get_orders(account_id= account_id)

    return open_orders

# トレード情報を取得
def Trades(prm):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    trades = oanda.get_trades(account_id= account_id)
    trades = pd.DataFrame(trades["trades"])

    return trades

# トレード履歴を取得
# count :　取得件数を入力
def HistricalTrade(prm,count):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    trade_hist = oanda.get_transaction_history(account_id= account_id,count= count)
    trade_hist = pd.DataFrame(trade_hist["transactions"])

    return trade_hist



# -------------注文する関数群----------------

# ストリーミング成行注文
# unitsは通貨量:　数字
# sideは買い側か売り側か等を入力(売り:"sell",買い:"buy")
# TakeProfit はとある利益が出た時点で決済をしてしまう処理
# StopLoss は損切りする値。思惑とは違う注文だった場合消してしまうためにある。
def Order(prm,Price,Units,Side,TakeProfit,StopLoss):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    order = oanda.create_order(account_id= account_id,
                               instrument = "USD_JPY",
                               price = Price,
                               units = Units,
                               side = Side,
                               takeProfit = TakeProfit,
                               stopLoss = StopLoss,
                               type = "market")

    return order

# 指値注文
# LimitTimeには有効期限を入力すること
# Priceには値段を入れる
# Unitsには通貨量をいれる
# Sideには買い側か売り側か入力(売り:"sell",買い:"buy")
def LimitOrder(prm,LimitTime,Price,Units,Side):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    limit_order = oanda.create_order(account_id= account_id,
                                     instrument = "USD_JPY",
                                     price = Price,
                                     units = Units,
                                     side = Side,
                                     expiry = LimitTime,
                                     type = "limit"
                                     )
    return limit_order

# 逆指値注文
# LimitTimeには有効期限を入力すること
# Priceには値段を入れる
# Unitsには通貨量をいれる
# Sideには買い側か売り側か入力(売り:"sell",買い:"buy")
def StopOrder(prm,LimitTime,Price,Units,Side):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    stop_order = oanda.create_order(account_id= account_id,
                                    instrument = "USD_JPY",
                                    price = Price,
                                    units = Units,
                                    side = Side,
                                    expiry = LimitTime,
                                    type = "stop"
                                    )
    return stop_order

# 成行注文(OCO注文)（利益確定と損切りの指定）
# High: 利益確定レート
# Low: 損切りレート
# Unitsには通貨量をいれる
# Sideには買い側か売り側か入力(売り:"sell",買い:"buy")
def MKOrder(prm,High,Low,Units,Side):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    order_mk = oanda.create_order(account_id= account_id,
                                  instrument="USD_JPY",
                                  units= Units,
                                  side= Side,
                                  takeProfit= High,
                                  stopLoss= Low,
                                  type="market")
    return order_mk

# 注文を変更する関数
# オープントレードからオーダーIDを取得してOrder_idにいれること
# Priceには希望価格を入力
# unitsには通貨量を入力
def ChangeOrder(prm,Order_id,Price,Units):
    environment = config[prm]["environment"]
    oanda = oandapy.API(environment=environment, access_token=api_key)
    changeorder = oanda.modify_order(account_id= account_id,
                                     instrument = "USD_JPY",
                                     order_id=Order_id,
                                     price=Price,
                                     units=Units)

    return changeorder

# if __name__ == "__main__":
#
#     test = OpenOrder()
#     print(test)