# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
#import pandas.io.data as web
import pandas_datareader.data as web




#-----------

#----init.dir

_rdat0="\\zwDat\\"
_rdatCN=_rdat0+"cn\\"
_rdatUS=_rdat0+"us\\"
_rdatInx=_rdat0+"inx\\"
_rdatMin=_rdat0+"min\\"

_rdatZW=_rdat0+"zw\\"


#----class
class zwDatX(object):
    def __init__(self,rs0=_rdat0):   #默认有此函数，自定义时运行自定义的。实例化时首次运行该函数
        self.rdat=rs0;        
        self.rdatCN=_rdatCN;
        self.rdatUS=_rdatUS;
        self.rdatInx=_rdatInx;
        self.rdatMin=_rdatMin;
        
        self.rdatZW=_rdatZW;
        self.rZWcnXDay=_rdatZW+"cnXDay\\"
        self.rZWcnDay=_rdatZW+"cnDay\\"
        self.rZWusDay=_rdatZW+"usDay\\"
        
        self.rXDay=rs0+"xday\\"
        self.rDay9=rs0+"day9\\"
        self.rDay=rs0+"day\\"
        
        self.rM05=_rdatMin+"m05\\"
        self.rM15=_rdatMin+"m15\\"
        self.rM30=_rdatMin+"m30\\"
        self.rM60=_rdatMin+"m60\\"
        
        self.code=""
        self.cname=""
        
    def prDat(self):        
        print('rdat',self.rdat)
        print('rdatCN',self.rdatCN)
        print('rdatUS',self.rdatUS)
        print('rdatInx',self.rdatInx)
        
        print('')
        print('rdatZW',self.rdatZW)
        print('rZWcnXDay',self.rZWcnXDay)
        print('rZWcnDay',self.rZWcnDay)
        print('rZWusDay',self.rZWusDay)
        
        print('')
        print('XDay',self.rXDay)
        print('Day9',self.rDay9)
        print('Day',self.rDay)
        
        print('')
        print('rdatMin',self.rdatMin)
        print('rM05',self.rM05)
        print('rM15',self.rM15)
        print('rM30',self.rM30)
        print('rM60',self.rM60)
        
        print('')
        print('code',self.code)
        print('name',self.cname)
        

        
#------------        
        
rs0="\\zwDat\\us\\"
#print('_rdat0=',_rdat0)
#rs0="\\zwDat\\cn\\"
qx=zwDatX(rs0);
qx.prDat();
