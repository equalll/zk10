# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import zwSys as zw         #zw.zwQuant
import zwTools as zwt
import zwQTBox as zwx

#======================
    

xlst=['aeti','egan','glng','simo']   
zwx.stkLibRd(xlst,'dat\\');
print(zw.stkLibCode)


xcod='aeti';xtim='2011-01-03'
x1=zwx.xbarGet8Tim(xcod,xtim);
print('x1\n',x1)

xcod='aeti';xtim='2012-01-03'
x2=zwx.xbarGet8Tim(xcod,xtim);
print('x2\n',x2)

#def xbarGet8Tim(xcod,xtim):
#def xbarGet8TimExt(xcod,xtim):
x2,df2=zwx.xbarGet8TimExt(xcod,xtim);
print('x2\n',x2)

print('df')
print(df2.head())
print(df2.tail())

