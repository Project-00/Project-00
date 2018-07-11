

#-*- coding: utf-8 -*-
import sys
sys.path.append(r'C:\Program Files\IronPython 2.7')
sys.path.append(r'C:\Program Files\IronPython 2.7\DLLs')
sys.path.append(r'C:\Program Files\IronPython 2.7\Lib')
sys.path.append(r'C:\Program Files\IronPython 2.7\Lib\site-packages')
 
import clr
clr.AddReference('mtrand.dll')
 
import oandapy
 
result = oandapy.sin(input)