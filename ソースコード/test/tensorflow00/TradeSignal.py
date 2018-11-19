# -*- coding: utf8 -*-

"""売買関数手順アイデア
１、２５日平均、１０日平均、５日平均の予測からそれぞれを曲線近似を用いて曲線式を生成する
２、それぞれの曲線式から直線の傾きを求めて進行方向を見る
３、if文で２５日平均の最上項が－の時と、＋の時で分岐させる（２通り）
４、if文で１０日平均と５日平均の現在の値を比べて分岐させる（２通り）
５、if文で予測込みの１０日平均の曲線の傾きと５日平均の曲線の傾きから分岐させる（４通り）
６、１６通りの分岐を使って売買を設定する

    ＋：
        ＋：
            ＋＋：
            ＋－：
            －＋：
            －－：
        －：
            ＋＋：
            ＋－：
            －＋：
            －－：
    
    －：
        ＋：
            ＋＋：
            ＋－：
            －＋：
            －－：
        －：
            ＋＋：
            ＋－：
            －＋：
            －－：
"""