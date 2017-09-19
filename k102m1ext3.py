# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np


import zwSys as zw  #::zwQT
import zwTools 

#----------code

    
def zw_anz_m1sub(xcod,rss,kstr):
    fss=rss+xcod+".csv";print(fss)
    nSum=0;nAdd=0;nDec=0;
    knum=int(kstr);knum2=knum+1;
    
    df = pd.read_csv(fss,index_col=0,parse_dates=[0],encoding='gbk') 
    df =df.rename(columns={'Close':'close'});df =df.sort_index();
    #
    _tim0=df.index[0];_ynum0=_tim0.year;
    _tim9=df.index[-1];_ynum9=_tim9.year+1;
    for ynum in range(_ynum0,_ynum9):
        ystr=str(ynum);_tim1x='-1';
        ystr2=ystr+"-"+kstr;  print(ystr2,len(df),knum)
        if knum==12:
            ystr3=ystr+"-"+kstr+'-31';
            df2=df[(df.index>=ystr2)&(df.index<=ystr3)]; 
        else:
            kstr2=str(knum2);
            if knum2<10:kstr2='0'+kstr2;
            ystr3=ystr+"-"+kstr2+'-01';
            df2=df[(df.index>=ystr2)&(df.index<ystr3)];
        print(ystr2,ystr3,len(df2))
        if (len(df2)>0):
            _tim1x=str(df2.index[0].month);
            if (len(_tim1x)<2):_tim1x='0'+_tim1x;  
        if (_tim1x==kstr): 
            df1=df2[ystr2];
            if (len(df1)>0):
                xd1a=df1.ix[0];xd1z=df1.ix[-1];nSum+=1;
                vd1a=xd1a['close'];vd1z=xd1z['close'];
                if (vd1z>vd1a):nAdd+=1
                else:nDec+=1;
                   

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
