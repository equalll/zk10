# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

#import ggplot

#import seaborn as sns

import zwSys as zw  #::zwQT
import zwQTBox as zwBox
import zwTools 

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
    df8.index=df['Month'];#df8.indexName='Month'
    return df8
    
    
      
def dr_cmap(fx,ftg9):
    cm8 = pd.read_csv('dat\\cor_maps.csv',encoding='gbk') 
    df2 = mx_sum_main(fx)
    df2.to_csv("tmp\\mx_"+ftg9+'.csv',encode='utf8');
    for xss in cm8['name']:
        df2.plot(kind='bar',colormap=xss,rot=0,figsize=(20,5)
            ,path_effects=[path_effects.withSimplePatchShadow()]);
        plt.axhline(50, color='r');    
        plt.legend(ncol=3,loc=2)
        plt.tight_layout()
        
        fss="tmp\\m1cor_"+xss+"_"+ftg9+".png";plt.savefig(fss);
        plt.show();print(xss,",",fss)
                 
#============main    


ftg9="cn";cnLst=['code','sz50','hs300','zz500','inxCN'];
dr_cmap(cnLst,ftg9);

ftg9="us";usLst=['xYah30sp','xYah100ns','xYah100sp','xYah600','xYah500sp','xYah']
dr_cmap(usLst,ftg9);

