# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
#import pandas.io.data as web
import pandas_datareader.data as web

#zw.Quant
import zwSys as zw  
import zwQTBox as zwBox


#--------
qx=zw.zwDatX(zw._rdatUS);

qx.code="AETI";fss="tmp\\"+qx.code+".csv";
zwBox.down_stk_yahoo010(qx,fss);

qx.code="EGAN";fss="tmp\\"+qx.code+".csv";
zwBox.down_stk_yahoo010(qx,fss)

qx.code="GLNG";fss="tmp\\"+qx.code+".csv";
zwBox.down_stk_yahoo010(qx,fss)

qx.code="SIMO";fss="tmp\\"+qx.code+".csv";
zwBox.down_stk_yahoo010(qx,fss)
