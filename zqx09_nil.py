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
        if xcod=='aeti':stknum=-2000;
        if xcod=='egan':stknum=-1000;
        if xcod=='glng':stknum=1000;
        if xcod=='simo':stknum=1000;
        #print('tim',xtim,dtim0,xcod,stknum,dprice);
    
    if xday==2:
        if xcod=='aeti':stknum=500;
        if xcod=='egan':stknum=500;
        if xcod=='glng':stknum=-2000;

    if xday==3:
        if xcod=='aeti':stknum=-500;
        if xcod=='egan':stknum=-500;
        if xcod=='glng':stknum=1000;
        
    return stknum

  
def tim0Trade_dataPre(qx,xnam0):    
    #设置当前策略的变量参数，此处是5、30日的MA日均线数据
    qx.staName=xnam0
    qx.rfRate=0.05;  #无风险年收益，一般为0.05(5%)，计算夏普指数等需要
    #qx.stkNum9=20000;   #每手交易，最多20000股
    #
    #按指定的时间周期，裁剪数据源
    #xtim0=parse('9999-01-01');xtim9=parse('1000-01-01');
    #xtim0=xtim0.strftime('%Y-%m-%d');xtim9=xtim9.strftime('%Y-%m-%d')
    #qx.qxTimSet(xtim0,xtim9)
    #zwx.stkLibSet8XTim(qx.xtim0,qx.xtim9);#    print('zw.stkLibCode',zw.stkLibCode)
    #============
    #---设置qxUsr用户数据
    qx.qxUsr=zwx.qxObjSet(qx.xtim0,0,qx.money,0);
    #----对各只股票数据，进行预处理，提高后期运算速度
    ksgn='adj close';
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
        print(d20.tail())    
        #---
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
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);    
    #
    qx.prTrdLib()
        
#==================main


#--------设置参数
xlst=['aeti','egan','glng','simo']   
qx=zwbt.bt_init(xlst,'dat\\','inv01',10000);
qx.dvix_k0,qx.dvix_k9=65,135
#
#---设置策略参数
qx.staVars=[5,30,'','']    
#---根据当前策略，对数据进行预处理
tim0Trade_dataPre(qx,'tim0Trade')
#
#---绑定策略函数&运行回溯主函数
qx.staFun=tim0Trad;
zwbt.zwBackTest(qx)
#
#  运行回溯结束，计算交易回报数据，绘制相关图表
bt_endRets(qx)

