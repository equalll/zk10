# -*- coding: utf-8 -*-
'''
   zw_tur.py
   tur海龟策略
   
'''

import numpy as np
import pandas as pd

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
    kmid8=[[xcod,ksgn,'xhigh','xlow']]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);
    #
    print('')
    print('每日交易推荐')
    print('::xtrdLib',qx.fn_xtrdLib)
    print(qx.xtrdLib.tail())
    #print(qx.xtrdLib)


#==================main
#--------init，设置参数
#rss='\\zwdat\\cn\\day\\'
rss='dat\\'
xlst=['600401']   #600401,*ST海润,*SThr 
qx=zwbt.bt_init(xlst,rss,'tur10',10000);
#
#---设置策略参数


#qx.staVars=[35,15,'2014-01-01','']  #  30,15,=14339.67,43.40 %
qx.staVars=[5,5,'2015-01-01','']  #  30,15,=14339.67,43.40 %
qx.debugMod=1
#qx.staFun=tur10; #---绑定策略函数&运行回溯主函数
qx.staFun=zwsta.tur10; #---绑定策略函数&运行回溯主函数
#---根据当前策略，对数据进行预处理
#zwsta.tur10_dataPre(qx,'sta00','close')
zwsta.tur10_dataPre(qx,'tur10','close')
#----运行回溯主程序

zwbt.zwBackTest(qx)
#----输出回溯结果
bt_endRets(qx)
'''
,最终资产价值 ,回报率

30,10,=9325.77, -6.74 %
20,10,=$12407.49, 24.07 %
10,10,=$12544.90,25.45 %
5,10,=$15057.73, 50.58 %
5,5,=$19511.12，95.11 %
'''