# -*- coding: utf-8 -*-

import numpy as np
import math
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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
    #qx.prQLib()
    #
    #-------计算交易回报数据
    zwx.zwRetTradeCalc(qx)
    zwx.zwRetPr(qx)
    #-------绘制相关图表，可采用不同的模板
    # 初始化绘图模板：dr_quant3x
    zwdr.dr_quant3x_init(qx,12,8);
    #  设置相关参数
    xcod=zw.stkLibCode[0];
    #ma1='ma_%d' %qx.staVars[0]
    ksgn,ksgn2,ksgn3,ksgn4,ksgn5=qx.priceWrk,'boll_up','boll_low','boll_ma','boll_std'
    kmid8=[[xcod,ksgn,ksgn2,ksgn3,ksgn4,ksgn5]]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);
    #
    print('')
    print('每日交易推荐')
    print('::xtrdLib',qx.fn_xtrdLib)
    print(qx.xtrdLib.tail())
   

#==================main

#--------设置参数
#xlst=['yhoo-201x']   
#qx=zwbt.bt_init(xlst,'dat\\','bbands',1000000);
xlst=['601999']   #出版传媒
qx=zwbt.bt_init(xlst,'\\zwdat\\cn\\day\\','bbands2',10000);
#
#---设置策略参数
qx.debugMod=1
#qx.stkNum9=200000;#20000
qx.staVars=[40,'2014-01-01','']    
#---根据当前策略，对数据进行预处理
zwsta.BBANDS_dataPre(qx,'bbands','close')
#---绑定策略函数&运行回溯主函数
qx.staFun=zwsta.BBANDS_sta;
zwbt.zwBackTest(qx)
#
bt_endRets(qx)
    
        
#---
