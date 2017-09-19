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
import zwQTBox as zwBox


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod,cash=10000):  #100w
        strategy.BacktestingStrategy.__init__(self, feed,cash)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()



#--------
cod="002739";#万达院线
fss="dat\\"+cod+".csv";
df=pd.read_csv(fss,encoding='gbk');
#df2=zwBox.zw_df2yhaoo(df);
df2=zwBox.df2yhaoo(df);
fss="dat\\"+cod+"_yh.csv";print(fss);
df2.to_csv(fss,encoding='utf-8')
#

# Load the yahoo feed from the CSV file
feed = yahoofeed.Feed()
#feed.addBarsFromCSV("orcl", "dat\\orcl-2000.csv")
#fss="dat\\"+cod+".csv";
feed.addBarsFromCSV("wanda", fss)


# Evaluate the strategy with the feed's bars.
myStrategy = SMACrossOver(feed, "wanda", 20)

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
plt.getInstrumentSubplot('wanda').addDataSeries("sma", myStrategy.getSMA())

# Run the strategy.
myStrategy.run()

plt.plot()

#==============================    
print("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult())
print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

