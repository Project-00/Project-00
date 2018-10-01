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


    OPEN = "OPEN"
    CLOSE = "CLOSE"
    HIGH = "HIGH"
    LOW = "LOW"


import sys
# 定数型を作成する関数
sys.modules[__name__] = _const()



# c = _const()
#
# print(c.OPEN)