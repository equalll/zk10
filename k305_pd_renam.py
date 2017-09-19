# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
import zwQTBox as zwBox


    
#============main    
mpl.style.use('seaborn-whitegrid');

cod="002739";#万达院线
fss="dat\\"+cod+".csv";print(fss);
df=pd.read_csv(fss,encoding='gbk');
print("原数据")      
print(df.head())      

df2=zwBox.df2yhaoo(df);
print("\nYhaoo格式")      
print(df2.head())

print('')
cod="ORCL-2000";
fss="dat\\"+cod+".csv";print(fss);
df=pd.read_csv(fss,encoding='gbk');
print("原数据")      
print(df.head())      

#df2=zwBox.zw_df2yhaoo(df);
df2=zwBox.df2cnstk(df);
print("\ncn中国A股格式")      
print(df2.head())

