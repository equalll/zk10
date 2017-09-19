import pandas as pd
from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import vwap
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

class VWAPMomentum(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, vwapWindowSize, threshold):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__vwap = vwap.VWAP(feed[instrument], vwapWindowSize)
        self.__threshold = threshold

    def getVWAP(self):
        return self.__vwap
        
    def onBars(self, bars):
        vwap = self.__vwap[-1]
        if vwap is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        price = bars[self.__instrument].getClose()
        notional = shares * price

        if price > vwap * (1 + self.__threshold) and notional < 1000000:
            self.marketOrder(self.__instrument, 100)
            self.info("++ %.2f,%.2f,$%.2f,$%.2f,$%.2f" % (vwap,shares,price,notional,self.getBroker().getCash() ))
        elif price < vwap * (1 - self.__threshold) and notional > 0:
            self.marketOrder(self.__instrument, -100)
            self.info("-- %.2f,%.2f,$%.2f,$%.2f,$%.2f" % (vwap,shares,price,notional,self.getBroker().getCash() ))

def ret2csv(ftg,retx):
    xd=retx.getReturns()
    x8=[];
    for x1 in xd:
        x8=x8+[x1];
    xs1=pd.Series(x8);
    print(xs1.tail())
    xs1.to_csv(ftg)  
    print(ftg)
    
    return xs1

def main():
    instrument = "aapl"
    vwapWindowSize = 5
    threshold = 0.01

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, "dat\\aapl-201x.csv")

    strat = VWAPMomentum(feed, instrument, vwapWindowSize, threshold)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    retAnalyzer = returns.Returns()
    strat.attachAnalyzer(retAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)

    
    plt = plotter.StrategyPlotter(strat, True, False, True)
    plt.getInstrumentSubplot(instrument).addDataSeries("vwap", strat.getVWAP())

    strat.run()
    plt.plot()

    #==============================    
    print("最终资产价值 Final portfolio value: $%.2f" % strat.getResult())
    print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
    print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

    
    #===
    fss='tmp\k408vwap_dret.csv'
    xs1=ret2csv(fss,retAnalyzer);        

#------------
main()
