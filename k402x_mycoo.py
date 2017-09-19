# -*- coding: utf-8 -*-
#  python2.7
#  
#  学员修改版
#  
import numpy as np
import pandas as pd
import matplotlib as mpl

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.utils import stats

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed):
        strategy.BacktestingStrategy.__init__(self, feed, 1000000) #Pat中设置初始资本

        # We wan't to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)
        
        # Place the orders to get them processed on the first bar.
        #设置各股票下单量
        orders = {
            "wanda": 297810,
            "lujiazui": 81266,
            "linggang": 11095,
            "zhouyan": 17293,
        }
        for instrument, quantity in orders.items():
            self.marketOrder(instrument, quantity, onClose=True, allOrNone=True)
            
    def onBars(self, bars):
        pass
#生成储存csv
def ret2csv(ftg):
    xd=retAnalyzer.getReturns()
    print 'type of xd is: ',type(xd)
    x8=[];
    for x1 in xd:
        x8=x8+[x1];
    xs1=pd.Series(x8);
    print(xs1.tail())
    xs1.to_csv(ftg)  
    print(fss)
    
    return xs1
    



    
# Load the yahoo feed from CSV files.
feed = yahoofeed.Feed()
"""
feed.addBarsFromCSV("wanda", "tmp\\002739_yh.csv")
feed.addBarsFromCSV("lujiazui", "tmp\\600663_yh.csv")
feed.addBarsFromCSV("linggang", "tmp\\600231_yh.csv")
feed.addBarsFromCSV("zhouyan", "tmp\\002046_yh.csv")
"""
#重定向读取CSV路径
feed.addBarsFromCSV("wanda", "dat\\002739_yh.csv")
feed.addBarsFromCSV("lujiazui", "dat\\600663_yh.csv")
feed.addBarsFromCSV("linggang", "dat\\600231_yh.csv")
feed.addBarsFromCSV("zhouyan", "dat\\002046_yh.csv")


# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed)

# Attach returns and sharpe ratio analyzers.
retAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(retAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
drawDownAnalyzer = drawdown.DrawDown()
myStrategy.attachAnalyzer(drawDownAnalyzer)


# Run the strategy
myStrategy.run()


# Print the results.
print("")
print( "最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult())
print( "年收益 Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print( "平均日收益率 Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100))
print( "日收益率方差 Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns())))
print( "夏普指数 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0)))
print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

print('')
fss='tmp\dret010.csv'
xs1=ret2csv(fss);

mpl.style.use('seaborn-whitegrid');
xs1.plot()
