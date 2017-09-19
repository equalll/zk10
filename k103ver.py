# -*- coding: utf-8 -*-

import sys

# py量化：三大件:pd,ts,zp,py量化分析的三个核心模块库，
import pandas as pd
import tushare as ts
#import zipline as zp
#
import talib as ta
import pyalgotrade as pat


# py数据分析：三大件,py数据分析，科学计算三个核心模块库，
import numpy as np
#import scipy as sp
import matplotlib as mpl #mpl
import matplotlib.pyplot as plt
#import seaborn as sns
#import ggplot as gpl
#
import numba as nb
import numexpr as ne  
#
import statsmodels as sm
import sklearn 
import theano 
import pymc
import nltk
import pygame
#import pattern
#import pyopencl


#zw.xxx
import zwSys as zw  #::zwQuant


#=====================

print("pandas ver:",pd.__version__)
print("tushare ver:",ts.__version__)
print("zipline ver:",zp.__version__)
print("");
print("talib ver:",ta.__version__)
print("pyalgotrade ver:",pat.__version__)


print("");
print("numpy ver:",np.__version__)
print("scipy ver:",sp.__version__)
print("statsmodels ver:",sm.__version__)

print("");
print("matplotlib ver:",mpl.__version__)
#print("seaborn ver:",sns.__version__)
#print("ggplot ver:",gpl.__version__)

print("");
print("sklearn ver:",sklearn.__version__)
print("theano ver:",theano.__version__)
print("pymc ver:",pymc.__version__)
print("nltk ver:",nltk.__version__)
print("numba ver:",nb.__version__)
print("numexpr ver:",ne.__version__)
print("pygame ver:",pygame.__version__)



print("");
#print("pyopenclk ver:",pyopencl.VERSION)
#print("pattern ver:",pattern.__version__)
print("zwQuant ver:",zw.__version__)
print("");
print("BLAS,Basic Linear Algebra Subprograms,即基础线性代数子程序库")
print("检验numpy等库是否使用了blas加速")
print("如果结果是：False，则表明实现了BLAS加速。")
fgBlas=(id(np.dot) == id(np.core.multiarray.dot))
print("fgBlas,",fgBlas)
