# -*- coding: utf-8 -*-
#  python2.7 版本
#  

import numpy as np
import pandas as pd

from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns

from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown

from pyalgotrade.stratanalyzer import trades
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

from pyalgotrade import plotter
import zwQTBox as zwx


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        strategy.BacktestingStrategy.__init__(self, feed, 1000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
        
    def getSMA(self):
        return self.__sma        

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


#--------数据格式转换，常用国内A股数据，转换为yahoo财经格式
cod="002739";#万达院线
cname='wanda';
fss="dat\\"+cod+".csv";
df=pd.read_csv(fss,encoding='gbk');
#df2=zwBox.zw_df2yhaoo(df);
df2=zwx.df2yhaoo(df);
cfn="dat\\"+cod+"_yh.csv";print(fss);
df2.to_csv(cfn,encoding='utf-8')

# Load the yahoo feed from the CSV file
feed = yahoofeed.Feed()
feed.addBarsFromCSV(cname,cfn)

# Evaluate the strategy with the feed's bars.
#myStrategy = SMACrossOver(feed, "orcl", 20)
myStrategy = MyStrategy(feed,cname, 15)

# Attach different analyzers to a strategy before executing it.
retAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(retAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
drawDownAnalyzer = drawdown.DrawDown()
myStrategy.attachAnalyzer(drawDownAnalyzer)
tradesAnalyzer = trades.Trades()
myStrategy.attachAnalyzer(tradesAnalyzer)

# ---set.plot
plt = plotter.StrategyPlotter(myStrategy, True, False, True)
plt.getInstrumentSubplot(cname).addDataSeries("sma", myStrategy.getSMA())

# Run the strategy.
myStrategy.run()
print "最终资产价值 Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

plt.plot()

#==============================    
print("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult())
print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))
