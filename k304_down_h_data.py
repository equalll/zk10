
# -*- coding: utf-8 -*-
import os
import tushare as ts
import pandas as pd
import matplotlib as mpl

import zwSys as zw  #::zwQT


#----------



def zw_down_stk_cn020(qx):
    xcod=qx.code;xd=[];tim0='1994-01-01'; 
    rss="tmp\\";fss=rss+xcod+'.csv';
    #-------------------
    xfg=os.path.exists(fss);xd0=[];
    if xfg:
        xd0=pd.read_csv(fss,index_col=0,parse_dates=[0],encoding='gbk') 
        xd0=xd0.sort_index(ascending=False);
        _xt=xd0.index[0];
        s2=str(_xt);tim0=s2.split(" ")[0]
        
    print('\n',xfg,fss);   
    #-----------    
    try:
        xd=ts.get_h_data(xcod,start=tim0,end=None,retry_count=5,pause=1)     #Day9
        #-------------
        if xd is not None:
            if (len(xd0)>0):         
                xd2 =xd0.append(xd)                
                #  flt.dup 
                xd2["index"]=xd2.index
                xd2.drop_duplicates(subset='index', keep='last', inplace=True);
                del(xd2["index"]);
                #xd2.index=pd.to_datetime(xd2.index)
                xd=xd2;
            
            xd.to_csv(fss,encoding='gbk');print(fss)
    except IOError: 
        pass    #skip,error
    
           
    return xd  
    
 
#----------
mpl.style.use('seaborn-whitegrid');
qx=zw.zwDatX(zw._rdatCN);
qx.code="002739";#万达院线
#qx.code="399107";#深证Ａ指
#qx.code="399001";#深证成指
#qx.code="sh";#深证成指



#qx.prDat();

#
df=zw_down_stk_cn020(qx)

df.index=pd.to_datetime(df.index)
df=df.sort_index(ascending=False);

df['close'].plot(figsize=(15,5),rot=20)
print(df.tail())
