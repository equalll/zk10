# -*- coding: utf-8 -*-

import sys
import os
import pandas as pd
import pip

#=============
plst=pip.get_installed_distributions();
print(plst[10])

df=pd.DataFrame();
df['<name>']=plst;
print(df.tail())
fss="tmp\\m100.csv";print("\n"+fss)
df.to_csv(fss,index=False)

