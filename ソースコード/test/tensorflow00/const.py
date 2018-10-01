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


import sys
# 定数型を作成する関数
def const(Name):
    sys.modules[__name__] = _const()

    # _const.START = "START"

    const.Name = str(Name)

    return const.Name

c = const

START = c("START")
CLOSE = c("CLOSE")
HIGH = c("HIGH")
LOW = c("LOW")

print(START)
print(CLOSE)
print(HIGH)
print(LOW)
