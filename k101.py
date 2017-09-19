# -*- coding: utf-8 -*-

import numpy as np

# =======================

def sta001(k,nyear,xd):
    d2=np.fv(k,nyear,-xd,-xd);
    d2=round(d2)
    return d2

    
# =======================

d40=1.4*40
print("d40,40 x 1.4=",d40)
d=sta001(0.05,40-1,1.4);
print("01保守投资模式，",d,round(d/d40))

d2=sta001(0.20,40-1,1.4);
print("02激进投资模式，",d2,round(d2/d40))

dk=round(d2/d)
print("dk,两者差别（xx倍）：",dk)




