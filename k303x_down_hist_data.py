# -*- coding: utf-8 -*-
import os
import tushare as ts
import pandas as pd
import matplotlib as mpl

#zw.xxx
import zwSys as zw  #::zwQT



#----------

def zw_down_stk_cn010(qx,xtyp="D"):
    """ xcod:股票代码
        xtyp：数据类型，9,Day9,简版股票数据，可下载到2001年，其他的全部是扩充版数据，只可下载近3年数据
            D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
            X=大盘、各种指数日k线 
    """
    xcod=qx.code;xd=[];tim0='2012-01-01';
    rss="tmp\\";fss=rss+xcod+"_"+xtyp+'.csv';
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
        xd=ts.get_hist_data(xcod,start=tim0,end=None,retry_count=5,pause=1,ktype=xtyp);
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
            
            xd.to_csv(fss,encoding='gbk')
    except IOError: 
        pass    #skip,error
    
           
    return xd  
    
 
#----------
mpl.style.use('seaborn-whitegrid');
qx=zw.zwDatX(zw._rdatCN);
qx.code="002739";#万达院线
#qx.prDat();

#
df=zw_down_stk_cn010(qx,"D")
#df=zw_down_stk_cn010(qx,"5")
df.index=pd.to_datetime(df.index)
df=df.sort_index(ascending=False);

df['close'].plot(figsize=(15,5),rot=-15)
print(df.tail())
