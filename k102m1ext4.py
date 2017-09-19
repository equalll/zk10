# -*- coding: utf-8 -*-
#  zw量化开源团队 
#  中文注释 我怎能不戏猫 （QQ： 316894075）
# 

import sys
import pandas as pd
import numpy as np


import zwSys as zw  #::zwQT
import zwTools 

#----------code

    
def zw_anz_m1sub(xcod,rss,kstr): #kstr表示月份
    fss=rss+xcod+".csv";print(fss) #读取的文件名
    nSum=0;nAdd=0;nDec=0; #所输入的月份的数量，上升数，下降数
    knum=int(kstr);knum2=knum+1; #当前月份；下一月份
    
    df = pd.read_csv(fss,index_col=0,parse_dates=[0],encoding='gbk') #读取文件
    df =df.rename(columns={'Close':'close'});df =df.sort_index();#按照指数（时间）排序
    #
    _tim0=df.index[0];_ynum0=_tim0.year; #第一年
    _tim9=df.index[-1];_ynum9=_tim9.year+1; #最后一年
    for ynum in range(_ynum0,_ynum9):
        ystr=str(ynum);_tim1x='-1';
        ystr2=ystr+"-"+kstr;  print(ystr2,len(df),knum)
        if knum==12: #如果是12月
            ystr3=ystr+"-"+kstr+'-31'; #年-月-日
            df2=df[(df.index>=ystr2)&(df.index<=ystr3)]; #选取该月交易日
        else:
            kstr2=str(knum2);#初始月份的下一个月
            if knum2<10:kstr2='0'+kstr2; #如05
            ystr3=ystr+"-"+kstr2+'-01'; #生成年-月-日格式
            df2=df[(df.index>=ystr2)&(df.index<ystr3)]; #选取该月交易日
        print(ystr2,ystr3,len(df2)) #上一月到下一月第一天的交易日总数
        if (len(df2)>0): #若存在交易日
            _tim1x=str(df2.index[0].month);
            if (len(_tim1x)<2):_tim1x='0'+_tim1x;  #对小于10的月份加上‘0’
        if (_tim1x==kstr):  
            df1=df2[ystr2];
            if (len(df1)>0):
                xd1a=df1.ix[0];xd1z=df1.ix[-1];nSum+=1; #df.ix[,],选取行（0），列（1）
                vd1a=xd1a['close'];vd1z=xd1z['close']; #收盘价
                if (vd1z>vd1a):nAdd+=1 #月尾收盘价大于月初收盘价（升）
                else:nDec+=1; #月尾收盘价小于月初收盘价（跌）
                   

    #print('nSum,nAdd,nDec,',nSum,nAdd,nDec); 
    return nSum,nAdd,nDec    
   

        
        
#============main        
qx=zw.zwDatX(zw._rdatCN);



cod="002739";#万达院线
#rss=qx.rZWcnDay;
rss=zw._rdatCN+'day\\'
kstr="01"
#zw_anz_m1sub(xcod,rss,kstr):
nSum,nAdd,nDec=zw_anz_m1sub(cod,rss,kstr);
print('nSum,nAdd,nDec',nSum,nAdd,nDec)
