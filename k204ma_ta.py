# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import zw_talib as ta 
#


#----------code.init
mpl.style.use('seaborn-whitegrid');

           
#============main    

fss="dat\\AAPL-201x.csv"
df=pd.read_csv(fss,encoding='gbk');
#df=ta.MA(df,5);
df=ta.MA(df,10,'Close');
df=ta.MA(df,30,'Close');
df=ta.MA(df,50,'Close');
print(df.tail())


df['Close'].plot(figsize=(15,5));
#df['ma_5'].plot();
df['ma_10'].plot();
df['ma_30'].plot();
df['ma_50'].plot();
plt.legend(ncol=5)









