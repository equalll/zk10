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
# Load the yahoo feed from the CSV file
feed = yahoofeed.Feed()
feed.addBarsFromCSV("orcl", "dat\\orcl-2000.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = SMACrossOver(feed, "orcl", 20)

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
plt.getInstrumentSubplot('orcl').addDataSeries("sma", myStrategy.getSMA())

# Run the strategy.
myStrategy.run()

plt.plot()



#==============================    
print("最终资产价值 Final portfolio value: $%.2f" % myStrategy.getResult())
print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

print("")
print("总交易 Total trades: %d" % (tradesAnalyzer.getCount()))
if tradesAnalyzer.getCount() > 0:
    profits = tradesAnalyzer.getAll()
    print("平均利润 Avg. profit: $%2.f" % (profits.mean()))
    print("利润方差 Profits std. dev.: $%2.f" % (profits.std()))
    print("最大利润 Max. profit: $%2.f" % (profits.max()))
    print("最小利润 Min. profit: $%2.f" % (profits.min()))
    returns = tradesAnalyzer.getAllReturns()
    print("平均收益率 Avg. return: %2.f %%" % (returns.mean() * 100))
    print("收益率方差 Returns std. dev.: %2.f %%" % (returns.std() * 100))
    print("最大收益率 Max. return: %2.f %%" % (returns.max() * 100))
    print("最小收益率 Min. return: %2.f %%" % (returns.min() * 100))

print("")
print("赢利交易 Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))
if tradesAnalyzer.getProfitableCount() > 0:
    profits = tradesAnalyzer.getProfits()
    print("平均利润 Avg. profit: $%2.f" % (profits.mean()))
    print("利润方差 Profits std. dev.: $%2.f" % (profits.std()))
    print("最大利润 Max. profit: $%2.f" % (profits.max()))
    print("最小利润 Min. profit: $%2.f" % (profits.min()))
    returns = tradesAnalyzer.getPositiveReturns()
    print("平均收益率 Avg. return: %2.f %%" % (returns.mean() * 100))
    print("收益率方差 Returns std. dev.: %2.f %%" % (returns.std() * 100))
    print("最大收益率 Max. return: %2.f %%" % (returns.max() * 100))
    print("最小收益率 Min. return: %2.f %%" % (returns.min() * 100))

print("")
print("亏损交易Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))
if tradesAnalyzer.getUnprofitableCount() > 0:
    losses = tradesAnalyzer.getLosses()
    print("平均亏损 Avg. loss: $%2.f" % (losses.mean()))
    print("亏损方差 Losses std. dev.: $%2.f" % (losses.std()))
    print("最大亏损 Max. loss: $%2.f" % (losses.min()))
    print("最小亏损 Min. loss: $%2.f" % (losses.max()))
    returns = tradesAnalyzer.getNegativeReturns()
    print("平均收益率 Avg. return: %2.f %%" % (returns.mean() * 100))
    print("收益率方差 Returns std. dev.: %2.f %%" % (returns.std() * 100))
    print("最大收益率 Max. return: %2.f %%" % (returns.max() * 100))
    print("最小收益率 Min. return: %2.f %%" % (returns.min() * 100))


    