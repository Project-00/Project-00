import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mongodb_read import mongodb_read
import sys
import const

# 定数呼び出し
c = sys.modules["const"]

# モンゴから呼び出し
Data = mongodb_read(c.STUDY_COL)
Data = Data.sort_values(by="time")
Data = Data.reset_index()
PreData = mongodb_read(c.PREDICTION_COL)
PreData = PreData.sort_values(by="time")
PreData = PreData.reset_index()

Data = Data.ix[:, ["time", "close"]]
PreData = PreData.ix[:, ["time", "close"]]

Data = Data[len(Data.index) - len(PreData.index) - 1:]

plt.figure()
ax = Data[-7:].plot(x="time",y="close")
PreData[-8:].plot(x="time",y="close" ,ax = ax)
print("描画")