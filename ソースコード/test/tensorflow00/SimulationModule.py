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

OrderNum = float(config["ORDERPARAMETER"]["OrderNumber"])

TiltBorder = float(config["ORDERPARAMETER"]["TiltBorder"])

TakeProfitBorder = float(config["ORDERPARAMETER"]["TakeProfitBorder"])

StopLossBorder = float(config["ORDERPARAMETER"]["StopLossBorder"])

print(OrderNum)
print(TiltBorder)
print(TakeProfitBorder)
print(StopLossBorder)

