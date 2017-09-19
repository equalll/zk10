# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

#import ggplot
import pandas as pd
#import seaborn as sns

import zwSys as zw  #::zwQT
import zwQTBox as zwBox
import zwTools as zwt

#----------code
mpl.style.use('seaborn-whitegrid');

def mx_sum_main(fx):    
    fx8=fx;    
    df8=pd.DataFrame(columns=fx8);
    for fx0 in fx8:
        fss="dat\\mx_"+fx0+".csv";print(fss);
        df=pd.read_csv(fss,encoding='gbk');
        df8[fx0]=df['kAdd'];
    df=df.rename(columns={'ksgn':'Month'});
    df8.index=df['Month'];
    return df8
    
#============main    

cnLst=['code','sz50','hs300','zz500','inxCN'];
df2 = mx_sum_main(cnLst)
df2.plot(kind='bar',colormap='hot',rot=0,figsize=(20,5));
plt.legend(ncol=3,loc=2)
plt.tight_layout()


usLst=['xYah30sp','xYah100ns','xYah100sp','xYah600','xYah500sp','xYah']
df2 = mx_sum_main(usLst)
df2.plot(kind='bar',colormap='hot',rot=0,figsize=(20,5));
plt.legend(ncol=3,loc=2)
plt.tight_layout()
