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
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'orcl')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);

    

#==================main

#--------设置参数
xlst=['orcl-2000']   
qx=zwbt.bt_init(xlst,'dat\\','sma',10000);
#
#---设置策略参数
qx.debugMod=1
qx.staVars=[5,15,'2000-01-01','2000-12-31']    
#---根据当前策略，对数据进行预处理
zwsta.SMA_dataPre(qx,'sma','adj close')
#---绑定策略函数&运行回溯主函数
qx.staFun=zwsta.SMA_sta;
zwbt.zwBackTest(qx)
#
bt_endRets(qx)


'''
最终资产价值 Final portfolio value: $974.53
累计回报率 Cumulative returns: -2.55 %
夏普比率 Sharpe ratio: -0.43
最大回撤率 Max. drawdown: 14.19 %
最长回撤时间 Longest drawdown duration: 277 days, 0:00:00
247    0.014118
248   -0.008701
249   -0.002341
250    0.003519
251   -0.018703
---
2000-01-26 ,BUY at $26.35,$25.41,$736.49
2000-01-28 ,Sell at $23.91,$25.42,$975.62
2000-02-03 ,BUY at $25.71,$25.31,$718.49
2000-02-22 ,Sell at $27.45,$27.51,$993.03
2000-02-23 ,BUY at $27.95,$27.79,$713.56
2000-03-31 ,Sell at $37.23,$37.98,$1085.90
2000-04-07 ,BUY at $38.86,$38.11,$697.31
2000-04-12 ,Sell at $36.19,$37.81,$1059.20
2000-04-19 ,BUY at $36.51,$35.68,$694.11
2000-04-20 ,Sell at $34.27,$35.44,$1036.86
2000-04-28 ,BUY at $36.45,$35.02,$672.35
2000-05-05 ,Sell at $34.36,$34.78,$1015.96
2000-05-08 ,BUY at $34.97,$35.08,$666.25
2000-05-09 ,Sell at $34.22,$34.99,$1008.42
2000-05-16 ,BUY at $36.04,$34.93,$647.97
2000-05-19 ,Sell at $33.43,$34.68,$982.30
2000-05-31 ,BUY at $34.01,$33.00,$642.17
2000-06-23 ,Sell at $37.52,$38.01,$1017.41
2000-06-27 ,BUY at $38.25,$38.23,$634.91
2000-06-28 ,Sell at $38.11,$38.32,$1015.96
2000-06-29 ,BUY at $38.11,$38.27,$634.91
2000-06-30 ,Sell at $37.32,$38.31,$1008.13
2000-07-03 ,BUY at $37.67,$38.30,$631.43
2000-07-05 ,Sell at $35.67,$38.01,$988.10
2000-07-21 ,BUY at $35.96,$35.25,$628.53
2000-07-24 ,Sell at $35.81,$34.97,$986.65
2000-07-26 ,BUY at $34.74,$34.98,$639.26
2000-07-28 ,Sell at $34.88,$34.85,$988.10
2000-08-01 ,BUY at $34.91,$34.91,$638.97
2000-08-02 ,Sell at $33.90,$34.86,$977.94
2000-08-04 ,BUY at $36.36,$35.08,$614.31
2000-09-11 ,Sell at $39.96,$40.45,$1013.93
2000-09-29 ,BUY at $37.78,$37.20,$636.14
2000-10-02 ,Sell at $37.03,$37.05,$1006.46
2000-10-20 ,BUY at $33.55,$31.79,$670.97
2000-10-31 ,Sell at $30.30,$31.50,$973.95
2000-11-20 ,BUY at $22.58,$25.95,$748.17
2000-11-21 ,Sell at $23.04,$25.38,$978.60
2000-12-01 ,BUY at $24.49,$23.54,$733.66
2000-12-15 ,Sell at $27.34,$25.82,$1007.04
2000-12-18 ,BUY at $27.86,$26.36,$728.43
2000-12-21 ,Sell at $25.83,$27.39,$986.72
2000-12-22 ,BUY at $28.21,$27.73,$704.64

Final portfolio value: $974.53

'''