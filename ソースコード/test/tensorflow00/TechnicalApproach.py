import numpy as np
import pandas as pd
from mongodb_read import mongodb_read
import sys
import const
import talib as ta


# 定数呼び出し
c = sys.modules["const"]

# np.arrayでデータ呼び出す
def npDataCall():

    df = mongodb_read(c.STUDY_COL)
    df = df.sort_values(by="time")
    df = df.reset_index()
    # df = df.ix[:, ["time", "close", "open", "high", "volume", "low", "fiveave", "tenave", "fiftave"]]
    df = df.ix[:, ["close"]]

    npdata = np.array(df,dtype= float)
    return npdata

# 縦の2次元のリストから横の1次元のリストへ変換
def changelist1(list):
    result = np.reshape(list, (-1,))
    return result

# 横の1次元のリストを2次元の縦のリストへ変換
def changelist2(list):
    result = np.reshape(list,(list.shape[0],1))
    return result

# トレンド系のテクニカル指標群(list型で返ってくる)
# 引数まとめ
# list : np.array配列またはリストを渡す
# time : 〇日平均等の何日に設定するかを渡す

# 単純移動平均
def SMA(list,time):
    result = ta.SMA(list, timeperiod = time)
    return result

# 三角移動平均
def TMA(list,time):
    result = ta.TRIMA(list,timeperiod = time)
    return result

# 指数平滑移動平均
def EMA(list,time):
    result = ta.EMA(list, timeperiod= time)
    return result

# 二重指数平滑移動平均
def DEMA(list,time):
    result = ta.DEMA(list, timeperiod= time)
    return result

# 三重指数移動平均
def TEMA(list,time):
    result = ta.T3(list, timeperiod = time)
    return result

# 加重移動平均
def WMA(list,time):
    result = ta.WMA(list, timeperiod= time)
    return result

# トレンドライン
def TRENDLINE(list):
    result = ta.HT_TRENDLINE(list)
    return result

# ボリンジャーバンド(3つの列(upper,middle,lower)で返ってくるので注意)
def BBANDS(list,time):
    result = ta.BBANDS(list,timeperiod = time, nbdevup=2, nbdevdn=2, matype=0)
    return result

# 変化率
def ROCP(list,time):
    result = ta.ROCP(list, timeperiod = time)
    return result

# モンメンタム
def MOM(list,time):
    result = ta.MOM(list, timeperiod = time)
    return result

# 相対力指数
def RSI(list,time):
    result = ta.RSI(list, timeperiod = time)
    return result

# MACD(3つの配列(MACD,signal,hist)で帰ってくる？)
def MACD(list):
    result = ta.MACD(list, fastperiod=12, slowperiod=26, signalperiod=9)
    return result

# アブソリュートプライスオシレーター
def APO(list,time):
    if (time == 15):
        result = ta.APO(list, fastperiod=(time - 10), slowperiod= time, matype=0)
    else:
        result = ta.APO(list, fastperiod=time, slowperiod=(time + 5), matype=0)
    return result

# パーセントプライスオシレーター
def PPO(list,time):
    if (time == 15):
        result = ta.PPO(list, fastperiod=(time - 10), slowperiod= time, matype=0)
    else:
        result = ta.PPO(list, fastperiod=time, slowperiod=(time + 5), matype=0)
    return result

# シャンデモメンタムオシレーター
def CMO(list,time):
    result = ta.CMO(list, timeperiod = time)
    return result

def AllMakeTechnical(list):
    Data = changelist1(list)

    sma5 = SMA(Data,5)
    sma10 = SMA(Data,10)
    sma15 = SMA(Data,15)
    tma5 = TMA(Data,5)
    tma10 = TMA(Data,10)
    tma15 = TMA(Data,15)
    ema5 = EMA(Data,5)
    ema10 = EMA(Data,10)
    ema15 = EMA(Data,15)
    dema5 = DEMA(Data,5)
    dema10 = DEMA(Data,10)
    dema15 = DEMA(Data,15)
    tema5 = TEMA(Data,5)
    tema10 = TEMA(Data,10)
    tema15 = TEMA(Data,15)
    wma5 = WMA(Data,5)
    wma10 = WMA(Data,10)
    wma15 = WMA(Data,15)
    trendline = TRENDLINE(Data)
    bbands5 = BBANDS(Data,5)
    bbands10 = BBANDS(Data,10)
    bbands15 = BBANDS(Data,15)
    rocp5 = ROCP(Data,5)
    rocp10 = ROCP(Data,10)
    rocp15 = ROCP(Data,15)
    mom5 = MOM(Data,5)
    mom10 = MOM(Data,10)
    mom15 = MOM(Data,15)
    rsi5 = RSI(Data,5)
    rsi10 = RSI(Data,10)
    rsi15 = RSI(Data,15)
    macd = MACD(Data)
    apo5 = APO(Data,5)
    apo10 = APO(Data,10)
    apo15 = APO(Data,15)
    ppo5 = PPO(Data,5)
    ppo10 = PPO(Data,10)
    ppo15 = PPO(Data,15)
    cmo5 = CMO(Data,5)
    cmo10 = CMO(Data,10)
    cmo15 = CMO(Data,10)

    return sma5,sma10,sma15,tma5,tma10,tma15,ema5,ema10,ema15,dema5,dema10,dema15,tema5,tema10,tema15,wma5,wma10,wma15,trendline, bbands5,bbands10,bbands15,rocp5,rocp10,rocp15,mom5,mom10,mom15,rsi5,rsi10,rsi15,macd,apo5,apo10,apo15,ppo5,ppo10,ppo15,cmo5,cmo10,cmo15


# # 試験用
# if __name__ == "__main__":
#     Data = npDataCall()
#     # Data = changelist1(Data)
#     # test = CMO(Data,10)
#     # result = changelist2(test)
#     sma5, sma10, sma15, tma5, tma10, tma15, ema5, ema10, ema15, dema5, dema10, dema15, tema5, tema10, tema15, wma5, wma10, wma15, trendline, bbands5, bbands10, bbands15, rocp5, rocp10, rocp15, mom5, mom10, mom15, rsi5, rsi10, rsi15, macd, apo5, apo10, apo15, ppo5, ppo10, ppo15, cmo5, cmo10, cmo15 = AllMakeTechnical(Data)
#
#     print(sma5)