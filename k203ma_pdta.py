# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import pandas_talib as pdta

#----------code.init
mpl.style.use('seaborn-whitegrid');

           
#============main    

fss="dat\\AAPL-201x.csv"
df=pd.read_csv(fss,encoding='gbk');
df=pdta.MA(df,5);
df=pdta.MA(df,10);
df=pdta.MA(df,30);
df=pdta.MA(df,50);
print(df.tail())


df['Close'].plot(figsize=(15,5));
df['MA_5'].plot();
df['MA_10'].plot();
df['MA_30'].plot();
df['MA_50'].plot();
plt.legend(ncol=5)









