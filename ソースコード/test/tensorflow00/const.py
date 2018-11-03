"""
Constant types in Python.
"""

## -*- coding: utf-8 -*-

# 定数型上書き封じエラー処理件定数作成クラス
class _const(object):
    class ConstError(TypeError):pass
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value
        def __delattr__(self, name):
            if name in self.__dict__:
                raise self.ConstError("Can't unbind const(%s)" % name)
            raise NameError(name)

    # DB情報
    STUDY_COL = "USD_JPY_RATE"
    PREDICTION_COL = "P_USD_JPY_RATE"
    IP_ADDRESS = "54.69.191.130"
    PORT = 27017
    ID = "autoTrade"
    PASS = "auto1103"

    # 4本値定数
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    HIGH = "HIGH"
    LOW = "LOW"

    # 取得形式
    YEAR = "Y"
    MONTH = "M"
    DAY = "D"

import sys
# 定数型を作成する関数
sys.modules["const"] = _const()


# --定数呼び出し方法概要--
#
# import const
# import sys
#
# c = sys.modules["const"]
#
# print(c.HIGH)