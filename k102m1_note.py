# -*- coding: utf-8 -*-
#  zw量化开源团队 
#  中文注释 我怎能不戏猫 （QQ： 316894075）
# 

import sys
import pandas as pd
import numpy as np


import zwSys as zw  #::zwQT
import zwTools as zwt

#----------code

    
def zw_anz_m1sub(xcod,rss,monStr):#kstr表示月份
    fss=rss+xcod+".csv";print(fss) #文件名
    nSum,nAdd,nDec=0,0,0 #输入的月份数，其中上升的月份，其中下跌的月份
    kmon=int(monStr); #当前月     print('@m1sub',kstr,fss)
    try:
        df = pd.read_csv(fss,index_col=0,parse_dates=[0],encoding='utf-8')  #读取文件，csv使用gbk编码
        df =df.rename(columns={'Close':'close'});df =df.sort_index(); #重命名close列；按指数（年月日）重排序
        #
        _tim0=df.index[0];_ynum0=_tim0.year; #解释时间模式，yy/mm/dd，这里提取了第一年
        _tim9=df.index[-1];_ynum9=_tim9.year+1; #最后一年+1
        #print('@t',_tim0,_tim9)
        for ynum in range(_ynum0,_ynum9): #遍历所有年份
            ystr=str(ynum);last_day=zwt.lastDay(ynum,kmon);#年份，每月的最后一天的日期
            dayStr='%02d'%last_day
            monStr1=''.join([ystr,'-',monStr,'-1'])       #当前月的第一天
            monStr9=''.join([ystr,'-',monStr,'-',dayStr]) #当前月的最后一天
            df2=df[(df.index>=monStr1)&(df.index<=monStr9)]; #选取年-月-01到年-月-月底之间
            #print('@y',ystr1,ystr9,ystr,len(df2))
            if (len(df2)>0): #若存在交易日（处理月份用）
                _kmon5='%02d' %df2.index[0].month; #选取交易日期中的月份，并转为string
                if (_kmon5==monStr):  #若上述月份为函数输入的变量
                    #df1=df2[ystr9]; #选取年-月，年为24行开始的遍历，月为kstr（输入的变量）
                    #if (len(df1)>0): #若存在交易日
                    xd1a=df2.ix[0];xd1z=df2.ix[-1];nSum+=1; #交易月份+1
                    vd1a=xd1a['close'];vd1z=xd1z['close']; #选取收盘价位
                    if (vd1z>vd1a):nAdd+=1 #比较收盘价位，判定升跌
                    else:nDec+=1;
                   
    except IOError: 
        pass;    #skip,error
        
    print('nSum,nAdd,nDec,',nSum,nAdd,nDec); 
    return nSum,nAdd,nDec    #返回值为交易月份数量，上升，下跌
    
def zw_stk_anz_m01(qx,finx0,rss,ksgn): #对每个股票运算一次上一个函数
    fss = qx.rdatInx+finx0+".csv";   #stk_code.csv,inxYahoo.csv
    print('f',fss)
    dinx = pd.read_csv(fss,encoding='utf-8')  #读取csv文件
    print(dinx.head())
    print('f2',fss)
    mx1={};mx1['finx']=finx0;mx1['ksgn']=ksgn;
    mx1['nSum']=0;mx1['nAdd']=0;mx1['nDec']=0;#字典，赋值
    #nSum=0;nAdd=0;nDec=0;
    xn9=len(dinx['code']);mx1['nstk']=xn9; #所读取的csv的行数（code列的长度）
    #遍历csv中的code名,i 是计数器变量
    for i,xcod in enumerate(dinx['code']):
        if (not isinstance(xcod,str)):xcod="%06d" %xcod;
   
        dSum,dAdd,dDec=zw_anz_m1sub(xcod,rss,ksgn); 
        
        mx1['nSum']=mx1['nSum']+dSum;        
        mx1['nAdd']=mx1['nAdd']+dAdd;
        mx1['nDec']=mx1['nDec']+dDec;
        print(i,'/',xn9,xcod,mx1);
    #
    print('xn9',xn9)    ;#    print(len(mx1['nAdd']))    
    mx1['kAdd']=np.round(mx1['nAdd']*100/ mx1['nSum']); #指数上升频率（估计概率）
    mx1['kDec']=np.round(mx1['nDec']*100/ mx1['nSum']); #指数下降频率（估计概率）
    
    
    return mx1
    
def zw_stk_anz_mx(qx,finx0,rss): #生成一个csv文件
    c10=["finx","ksgn","nstk",'nSum','nAdd','nDec','kAdd','kDec']; #csv的第一列
    df=pd.DataFrame(columns=c10); #定义dataframe
    ftg="tmp\\mx_"+finx0+".csv";print(ftg)  #打印csv文件名
    
    for i in range(12):
        ksgn="%02d" %(i+1);
        #ksgn=str(i+1);#if i<9:ksgn='0'+ksgn; #1到12月
        
        #print(ksgn)    
        mx1=zw_stk_anz_m01(qx,finx0,rss,ksgn); #利用上一个函数生成一个dataframe,
        
        ds1=pd.Series(mx1,index=c10); #生成一个pandas中的series
        ds2=ds1.T; #.T=转置（矩阵转置）
        df=df.append(ds2,ignore_index=True);#在df中加上ds2
        df.to_csv(ftg,index=False,encode='utf8'); #保存为csv，utf8编码
        
            
def zw_stk_anz_mx_all(qx,xlst):    #遍历指定list中的股票
    for fx in xlst:
        if (fx.find('Yah')>0):
            #rss=qx.rZWusDay
            rss=qx.rdat+'\\us\\day\\'
        else:
            if (fx=='inx_code'):rss=qx.rdat+'\\cn\\xday\\' #rss=qx.rZWcnXDay
            else:rss=qx.rdat+'\\cn\\day\\' #rss=qx.rZWcnDay
            
        finx0=fx; #生成文件名
        zw_stk_anz_mx(qx,finx0,rss); #用上一个函数生成csv文件
        
        
#============main        
qx=zw.zwDatX(zw._rdat0);


uslst=['inxYahoo30sp','inxYahoo100ns','inxYahoo100sp','inxYahoo600','inxYahoo500sp','inxYahoo']
zw_stk_anz_mx_all(qx,uslst)

cnlst=['inx_code','stk_sz50','stk_hs300','stk_zz500','stk_code','stk_code'];
zw_stk_anz_mx_all(qx,cnlst)


