import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_exchange = pd.read_csv('exchange.csv',encoding="cp932", header=1, names=["date", "USD", "rate"],
                         skipinitialspace=True, parse_dates=True)

df_exchange

print(df_exchange)
