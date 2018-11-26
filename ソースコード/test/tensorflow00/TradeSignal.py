# -*- coding: utf8 -*-

"""売買関数手順アイデア
１、１５日平均、１０日平均、５日平均の予測からそれぞれを曲線近似を用いて曲線式を生成する
２、それぞれの曲線式から傾きを求めて進行方向を見る

最小二乗法あたりで近似曲線描いてくれて良し
https://qiita.com/ishizakiiii/items/72be4ce16a10f97d6183

単純な３つの値から傾きを見ると、極地の折り返しで引っかかると思うので曲線から接戦を求めたほうがたぶん確実

７、買った時の売った時の値段を別の変数に登録すること。

http://www.fx-soken.co.jp/tech/

    短期＞中期＞長期
    短期＞長期＞中期
    中期＞短期＞長期
    中期＞長期＞短期
    長期＞短期＞中期
    長期＞中期＞短期

"""