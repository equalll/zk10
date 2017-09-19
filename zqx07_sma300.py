# -*- coding: utf-8 -*-
# 
#  

import numpy as np
import math
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#from pinyin import PinYin

from dateutil.parser import parse
from dateutil import rrule
import datetime as dt

#zwQuant
import zwSys as zw
import zwTools as zwt
import zwQTBox as zwx
import zwQTDraw as zwdr
import zwBacktest as zwbt
import zwStrategy as zwsta

import zw_talib as zwta
#=======================    
      
def bt_endRets(qx):            
    #---ok ，测试完毕
    # 保存测试数据，qxlib，每日收益等数据；xtrdLib，交易清单数据
    #qx.qxLib=qx.qxLib.round(4)
    qx.qxLib.to_csv(qx.fn_qxLib,index=False,encode='utf-8')
    qx.xtrdLib.to_csv(qx.fn_xtrdLib,index=False,encode='utf-8')
    qx.prQLib()
    #
    #-------计算交易回报数据
    zwx.zwRetTradeCalc(qx)
    zwx.zwRetPr(qx)
    
    #-------绘制相关图表，可采用不同的模板
    # 初始化绘图模板：dr_quant3x
    zwdr.dr_quant3x_init(qx,12,8);
    #  设置相关参数
    xcod=zw.stkLibCode[0];ksgn=qx.priceBuy;
    #xcod='glng';ksgn=qx.priceBuy;
    #kmid8=[['aeti',ksgn],['egan',ksgn],['glng',ksgn,'ma_5','ma_30'],['simo',ksgn,'ma_5','ma_30']]   
    ma1='ma_%d' %qx.staVars[0]
    ma2='ma_%d' %qx.staVars[1]
    kmid8=[[xcod,qx.priceWrk,ma1,ma2]]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'','hs300')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);

    

#==================main

#--------设置参数
rss='dat\\'  #rss='\\zwdat\\cn\\day\\'
xlst=['600401']   #600401,*ST海润
qx=zwbt.bt_init(xlst,rss,'sma',10000);
#000300,沪深300,2005-01-01
qx.stkInxCode,qx.stkInxName,qx.stkInxCName='000300','hs300','沪深300'

#
#---设置策略参数
qx.debugMod=0
#qx.staVars=[5,15,'2015-01-01','']    
qx.staVars=[5,15,'2015-01-01','']    
#---根据当前策略，对数据进行预处理
zwsta.SMA_dataPre(qx,'sma','close')
#---绑定策略函数&运行回溯主函数
qx.staFun=zwsta.SMA_sta;
zwbt.zwBackTest(qx)
#
bt_endRets(qx)

