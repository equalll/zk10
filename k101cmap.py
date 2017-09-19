# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt


# =======================
mpl.style.use('seaborn-whitegrid');


def sta001(k,nyear,xd):
    d2=np.fv(k,nyear,-xd,-xd);
    d2=round(d2)
    
    return d2
        
        
def dr_cmap(_dat):
    fss='dat\\cor_maps.csv'
    cm8 = pd.read_csv(fss,encoding='gbk') 
    i=0;
    for xss in cm8['name']:
        plt.figure()
        _dat.plot(colormap=xss)
        fss="tmp\\k101cor_"+xss+".png";plt.savefig(fss);
        i+=1;print(i,xss,",",fss)
        plt.show()
                
        
# =======================


dx05=[sta001(0.05,x,1.4) for x in range(0,40)]
dx10=[sta001(0.10,x,1.4) for x in range(0,40)]
dx15=[sta001(0.15,x,1.4) for x in range(0,40)]
dx20=[sta001(0.20,x,1.4) for x in range(0,40)]

df=pd.DataFrame(columns=['dx05','dx10','dx15','dx20']);
df['dx05']=dx05;df['dx10']=dx10;
df['dx15']=dx15;df['dx20']=dx20;
print(df.tail())


dr_cmap(df)



    
    