# -*- coding: utf-8 -*-

#zwQuant
import zwSys as zw
import zwQTBox as zwx

#=======================    

qx=zw.zwQuantX('rdInx',1000);
qx.stkInxRDat='\\zwdat\\cn\\xday\\'    #大盘指数数据源路径
#大盘指数代码,名称拼音,中文名称
qx.stkInxCode,qx.stkInxName,qx.stkInxCName='000001','sh001','上证指数'

#读取大盘指数
zwx.stkInxLibRd(qx)

#输出大盘指数
print(zw.stkInxLib)

#切割大盘指数
zwx.stkInxLibSet8XTim(qx,'2015-01-01','2016-04-05')

#输出大盘指数
print(zw.stkInxLib)
