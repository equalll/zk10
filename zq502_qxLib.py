# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import zwSys as zw         #zw.zwQuant
import zwQTBox as zwx

#======================
pd.set_option('display.width', 450)
    
qx=zw.zwQuantX('xbar',1000000); #100w
qx.priceCalc,qx.priceWrk,qx.priceBuy='close','close','close'
xlst=['aeti','egan','glng','simo']   
zwx.stkLibRd(xlst,'dat\\');
#print(zw.stkCode)
#
xtim='2011-01-03';
qx.qxTim0SetVar(xtim); 
qx.qxUsr=zwx.qxObjSet(qx.xtim0,0,qx.money,0);
#
qx.stkCode='simo';
qx.stkNum=100;
xfg,qx.xtrdChk=zwx.xtrdChkFlag(qx)
zwx.xtrdLibAdd(qx)
qx.qxTim9SetVar(xtim)

qx.prQLib()

