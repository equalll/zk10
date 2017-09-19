# -*- coding: utf-8 -*-

#zwQuant
import zwSys as zw
import zwQTBox as zwx
import zwBacktest as zwbt

#=======================    
rss='dat\\'  #rss='\\zwdat\\cn\\day\\'
xlst=['600401']   #600401,*ST海润
qx=zwbt.bt_init(xlst,rss,'inx',10000);
#000300,沪深300,2005-01-01
qx.stkInxCode,qx.stkInxName,qx.stkInxCName='000300','hs300','沪深300'

#读取大盘指数
zwx.stkInxLibRd(qx)


#切割大盘指数
zwx.stkInxLibSet8XTim(qx,qx.xtim0,qx.xtim9)

#输出大盘指数
print(zw.stkInxLib)

