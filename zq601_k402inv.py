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

#----策略函数    


def tim0Trad(qx):
    '''
        tim0Trad(qx):
        零点交易策略，可看做是基于时间的：事件模式·回溯测试
        【输入】
            qx.stkCode，当前交易的股票代码
            qx.xtim，当前交易的时间
        【输出】
            srkNum，当前股票代码xcod，交易的股票数目：>0，买入；<0,卖出;=0,不交易
    '''    
    stknum=0;    
    xtim=qx.xtim;
    xcod=qx.stkCode;
    xday=rrule.rrule(rrule.DAILY,dtstart=qx.DTxtim0,until=parse(xtim)).count()
    #第一天
    if xday==1:
        #print('xd',xday,dtim0,xtim)
        #按预设订单，下单购买股票
        if xcod=='aeti':stknum=297810;
        if xcod=='egan':stknum=81266;
        if xcod=='glng':stknum=11095;
        if xcod=='simo':stknum=17293;
        #print('tim',xtim,dtim0,xcod,stknum,dprice);
    
    if xday==-2:
        if xcod=='aeti':stknum=500;
        if xcod=='egan':stknum=500;
        if xcod=='glng':stknum=-1000;

    if xday==-3:
        if xcod=='aeti':stknum=-500;
        if xcod=='egan':stknum=-500;
        if xcod=='glng':stknum=1000;
        
    return stknum

  
def tim0Trade_dataPre(qx,xnam0,ksgn0):    
    zwx.sta_dataPre0xtim(qx,xnam0);
    #-------
    ksgn,qx.priceCalc=ksgn0,ksgn0;  #'adj close';
    for xcod in zw.stkLibCode:
        d20=zw.stkLib[xcod];
        #  计算交易价格kprice和策略分析采用的价格dprice,kprice一般采用次日的开盘价
        #d20['dprice']=d20['open']*d20[ksgn]/d20['close']
        d20['dprice']=d20[ksgn]
        #d20['kprice']=d20['dprice'].shift(-1)
        d20['kprice']=d20['dprice']
        #
        d=qx.staVars[0];d20=zwta.MA(d20,d,ksgn);
        d=qx.staVars[1];d20=zwta.MA(d20,d,ksgn);
        #
        zw.stkLib[xcod]=d20;
        if qx.debugMod>0:
            print(d20.tail())    
            fss='tmp\\'+qx.prjName+'_'+xcod+'.csv'
            d20.to_csv(fss)        
    

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
    #  设置绘图相关参数
    xcod='glng';ksgn=qx.priceBuy;
    kmid8=[['aeti',ksgn],['egan',ksgn],['glng',ksgn,'ma_5','ma_30'],['simo',ksgn,'ma_5','ma_30']]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'<xcod>')
    #zwdr.dr_quant3x(qx,xcod,'val',kmid8,'')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);    
    
 
   
#==================main


#--------设置参数
xlst=['aeti','egan','glng','simo']   
qx=zwbt.bt_init(xlst,'dat\\','inv01',1000000);
#
#---设置策略参数
qx.staVars=[5,30,'','']    
qx.debugMod=1
#---根据当前策略，对数据进行预处理
tim0Trade_dataPre(qx,'tim0Trade','adj close')
#
#---绑定策略函数&运行回溯主函数
qx.staFun=tim0Trad;
zwbt.zwBackTest(qx)
#
#  运行回溯结束，计算交易回报数据，绘制相关图表
bt_endRets(qx)

#
'''
:: k402_compinv01.py
最终资产价值 Final portfolio value: $1524087.19
年收益 Anual return: 52.41 %
平均日收益率 Average daily return: 0.17 %
日收益率方差 Std. dev. daily return: 0.0122

夏普指数 Sharpe ratio: 2.28
最大回撤率 Max. drawdown: 11.47 %
最长回撤时间 Longest drawdown duration: 82 days, 0:00:00

247    0.005510
248    0.001400
249   -0.017165
250    0.010841
251   -0.004488
dtype: float64
tmp\dret010.csv

'''