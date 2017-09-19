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
    xcod=zw.stkLibCode[0];
    #xcod='glng';ksgn=qx.priceBuy;
    #kmid8=[['aeti',ksgn],['egan',ksgn],['glng',ksgn,'ma_5','ma_30'],['simo',ksgn,'ma_5','ma_30']]   
    ma1='ma_%d' %qx.staVars[0]
    #ma2='ma_%d' %qx.staVars[1]
    ksgn=qx.priceWrk;
    kmid8=[[xcod,ksgn,ma1]]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'apple')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);

   

#==================main

#--------设置参数
xlst=['aapl-201x']   
qx=zwbt.bt_init(xlst,'dat\\','cma',1000000);
#
#---设置策略参数
qx.debugMod=1
qx.staVars=[163,'2011','2013']    
#---根据当前策略，对数据进行预处理
zwsta.CMA_dataPre(qx,'cma','adj close')
#---绑定策略函数&运行回溯主函数
qx.staFun=zwsta.CMA_sta;
zwbt.zwBackTest(qx)
#
bt_endRets(qx)
    
    
    

'''
Sharpe ratio: 1.12
最终资产价值 Final portfolio value: $1565183.40
累计回报率 Cumulative returns: 56.52 %
夏普比率 Sharpe ratio: 1.12
最大回撤率 Max. drawdown: 15.64 %
最长回撤时间 Longest drawdown duration: 128 days, 0:00:00
--


2011-11-28 00:00:00 strategy [INFO] above: $1000000.00,$49.76,48.64,18086
2011-11-29 00:00:00 strategy [INFO] BUY at $49.72,$48.67,$100708.79

2012-10-25 00:00:00 strategy [INFO] below: $100708.79,$80.99,81.00
40
2012-10-26 00:00:00 strategy [INFO] Sell at $49.72,$81.06,$1565183.40

2011-11-28 00:00:00 strategy [INFO] above: $1000000.00,$49.76,48.64,18086
2011-11-29 00:00:00 strategy [INFO] BUY at $49.72,$48.67,$100708.79

2012-10-25 00:00:00 strategy [INFO] below: $100708.79,$80.99,81.00
2012-10-26 00:00:00 strategy [INFO] Sell at $49.72,$81.06,$1565183.40
('pos,', {'aapl': 18086})

'''