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
AccountData = ResponsAccountDetail(c.DEMO)
Balance = AccountData["balance"] # 残高

"""
必要な引数
Now_Rate : 現在の値
queue : ７２０個単位の現在値の集合
Unit :　通貨量（取引金額は現在の値段×通貨量で決まる）
StandardClose : 21時点のCloseの予測値

"""

"""
基本は順張りしか使わないようにする
今のところ逆張りは考えない
作りたい処理
1,残高、予測値を使って一度に取引をする量を決める処理
2,第一象限と第三象限を見極めるための処理
3,ボリンジャーバンドの範囲で信頼度を設定しておく

4,上昇相場での振る舞い
右肩上がりにトレンドが動き続けてる間に行う処理
順張りなら買い
予測に基づいて、予測値より小さい値の時に買い、予測値より大きい値の時に売りに入るようにする
5,下落相場での振る舞い
順張りなら売り
予測に基づいて、予測値より小さい時に買い、予測より大きい値の時売り

どちらにしろ予測値より小さい時に買い、大きい時に売りを徹底する。

判断の順番
１、現在の値段の位置が予測した最終的なcloseよりも上か下か
２、１５単位を使って現在の値動きの傾きを見る（15個の最新データを選抜く）
→closeよりも上で下降傾向の時、順張り売りポジションを選択
→closeよりも上で上昇傾向の時、ボリンジャーバンドを見る、順張り買い　３へ
→closeよりも下で上昇傾向の時、順張り買いポジションを選択
→closeよりも下で下降傾向の時、ボリンジャーバンドを見る、順張り売り　３へ
傾きの度合いが平坦な場合は　４へ
３、６０単位を使ってボリンジャーバンドを見た時に区間を超えているかどうかを見る
→超えている→勢いがあり、買われすぎ、売られすぎが起きているので対処
→超えていない場合は、バンドの幅の広さを見て、拡大してるときは大きなトレンド形成があるので追いかける
→収束してる場合は触れないように心がける

４、RSIが30以下から反転上昇したら買い、70以上から反転下落したら売り（取引量は小さめにする）
    横ばいの判定を傾きが0.3~-0.3の幅に存在しているときという風に断定しておく。

※残高がある一定値を下回った時点で買いの自動取引を行わないようにする処理も追加

"""
# 実験痕
# list = np.array([1,0,3,1,5,3,7,5,9,7,11,9,13,11,15,13,17,15,19,17,21,19,23],dtype = "f8")
#
# Data = changelist1(list)
# Data2 = changelist2(list)
# trend = BBANDS(Data,5)
#
# print(trend)

def TradeOrder(Now_Rate,queue,Units,StandardClose):
    UseList = [queue[i][0] for i in range(len(queue)-60,-1)]
    UseList = changelist1(UseList)

    # 単回帰のためのList
    TiltList1 = [queue[i][0] for i in range(len(queue)-15,-1)]      # Y軸用の現在の値集合（目的関数）
    TiltList2 = [queue[i][1] for i in range(len(queue)-15,-1)]      # X軸用の時間の集合（説明関数）
    TiltList1 = changelist1(TiltList1)      # 1次元のリストに直している
    TiltList2 = changelist1(TiltList2)      # 1次元のリストに直している

    lr = LinearRegression()
    X = TiltList2
    Y = TiltList1
    lr.fit(X,Y)

    Tilt = lr.coef_[0] # 傾き

    # 売り側か買う側か細かく事象を決めておく処理
    # 現在の値が予測よりも上の時の処理
    if Now_Rate >= StandardClose:
        # 傾きが上を向いているとき
        if Tilt >= 0.3:
            Band = BBANDS(UseList,5)
            # 96%の信頼区間を超えてるのでこの先も伸びる想定（）
            if Band[0][-1] <= Now_Rate:
                return
            # 96%の信頼区間の範疇なので何時反転しても良いように売利に入る（保守的な利益の追求）
            else:
                Side = "sell"
        # 傾きが横ばいで不安定の時、逆行現象のシグナルを見つける（結局下へ向かうのが分かる）
        elif (Tilt < 0.3) and (Tilt > -0.3):
            RsiScore = RSI(UseList,14)
            # 今の動きの最高値付近を叩いてる状態なので反転に備えて売りに入る
            if RsiScore > 80:
                Side = "sell"
            # 横ばいが続くならば状況が分からないので触らないでおく
            else:
                return
        # 傾きが下を向いているとき、素直に予測より上の間だけさっさと売ってしまう
        else:
                Side = "sell"

    # 現在の値が予測よりも下の時の処理
    else:
        # 傾きが上を向いているとき、素直に予測より下の間だけ買っておく
        if Tilt >= 0.3:
            Side = "buy"
        # 傾きが横ばいで不安定の時、逆行シグナルを見つける（結局上に向かうのが分かる）
        elif (Tilt < 0.3) and (Tilt > -0.3):
            RsiScore = RSI(UseList,14)
            # 売値の下限付近を叩いてる状態なので反転に備えて買っておく
            if RsiScore < 20:
                Side = "buy"
            # 横ばいが続くならば状況が分からないので触らないようにしておく
            else:
                return
        # 傾きが下を向いているとき
        else:
            Band = BBANDS(UseList,5)
            # 信頼区間96%を超えてる場合はまだ下がり続けるので下がりきるまで触らない
            if Band[2][-1] <= Now_Rate:
                return
            # 信頼区間96%の範囲内ならば、反転を考慮して安いうちに買っておく
            else:
                Side = "buy"

    # 預金が十二分にあるとき動くようにする。資金が無ければ注文はしない。
    if (Side == "buy") and (Now_Rate * Unit < Balance):
        # 注文を行う処理
        Order(c.DEMO,Now_Rate,Units,Side)
    elif (Side == "sell") and (Now_Rate * Unit < Balance):
        Order(c.DEMO, Now_Rate, Units, Side)
    else:
        return

    return