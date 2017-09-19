# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import zwSys as zw         #zw.zwQuant
import zwTools as zwt
import zwQTBox as zwx

#======================


xlst=['aeti','egan','glng','simo']   
zwx.stkLibRd(xlst,'dat\\');
print(zw.stkLibCode);
xcod=zw.stkLibCode[0]
d2=zw.stkLib[xcod]
print('\nd2',xcod)
print(d2.head())

#
print('')
xlst=['@inx\\inx_code.csv']   
zwx.stkLibRd(xlst,'\\zwDat\\cn\\xday\\');
print(zw.stkLibCode);
xcod=zw.stkLibCode[0]
d2=zw.stkLib[xcod]
print('\nd2',xcod)
print(d2.head())

