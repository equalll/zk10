# -*- coding: utf-8 -*-

#zwQuant
import zwSys as zw
import zwQTBox as zwx
import zwBacktest as zwbt

#=======================    
rss='dat\\'  #rss='\\zwdat\\cn\\day\\'
xlst=['600401']   #600401,*ST海润
qx=zwbt.bt_init(xlst,rss,'inx',10000);

#读取大盘指数
qx.stkInxCode,qx.stkInxName,qx.stkInxCName='000001','sh001','上证指数'
zwx.stkInxLibRd(qx)


#切割大盘指数
#zwx.stkInxLibSet8XTim(qx,qx.xtim0,qx.xtim9)
qx.staVars=[0,'','']
zwx.sta_dataPre0xtim(qx,'inx')
    
#输出大盘指数
print(zw.stkInxLib)

