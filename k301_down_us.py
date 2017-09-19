# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
#import pandas.io.data as web
import pandas_datareader.data as web

#zw.Quant
import zwSys as zw  
import zwQTBox as zwx

 
#-----------



def zw_down_yahoo8code(qx):
    try:
        xcod=qx.code;
        xdat= web.DataReader(xcod,"yahoo",start="1/1/1900");
        fss=qx.rDay+xcod+".csv";print(fss);
        xdat.to_csv(fss);
    except IOError: 
        pass    #skip,error
    
        
#------------        
        

qx=zw.zwDatX(zw._rdatUS);
qx.prDat();

#
code='USA';qx.code=code;qx.rDay="tmp\\";
zw_down_yahoo8code(qx);
    