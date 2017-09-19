# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

 
#zwQuant
import zwSys as zw  
import zwQTBox as zwBox
 
#-----------

        
def zw_stk_xedit_all(qx,finx,rsr,rtg):
    dinx = pd.read_csv(finx,index_col=False,encoding='gbk') 
    
    i=0;xn9=len(dinx['code']);
    for xcod in dinx['code']:
        i+=1;print("\n",i,"/",xn9,"code,",xcod)
        if (not isinstance(xcod,str)):xcod="%06d" %xcod
        qx.code=xcod;
        fss=rsr+xcod+'.csv';
        if os.path.exists(fss):
            df= pd.read_csv(fss,index_col=0,parse_dates=True,encoding='gbk') 
            d30=zwBox.xedit_zwXDat(df)
            fss=rtg+xcod+'.csv';print(fss);
            d30.to_csv(fss,encoding='gbk');
            
        
    
#============main        

#    运行前，请在zwdat建立以下3个数据目录
#    \zwDat\zw\cnDay\
#    \zwDat\zw\cnXDay\
#    \zwDat\zw\usDay\
#    作为输出目录
#

    
#------init

qdat=zw.zwDatX(zw._rdatCN);
qdat.prDat();

#-----------        
#   cnInx
finx=qdat.rdatInx+'inx_code.csv';
rsr=qdat.rdatCN+"XDay\\"
rtg=qdat.rZWcnXDay  #"\zwDat\zw\cnXDay\"    
zw_stk_xedit_all(qdat,finx,rsr,rtg);

#   cnSTK
finx=qdat.rdatInx+'stk_code.csv';
rsr=qdat.rdatCN+"Day\\"
rtg=qdat.rZWcnDay   #"\zwDat\zw\cnDay\"    
#zw_stk_xedit_all(qdat,finx,rsr,rtg);


#  usSTK
finx=qdat.rdatInx+'inxYahoo.csv';
rsr=qdat.rdatUS+"Day\\"
rtg=qdat.rZWusDay   #"\zwDat\zw\usDay\"
zw_stk_xedit_all(qdat,finx,rsr,rtg);        

