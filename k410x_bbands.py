from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
#from pyalgotrade.technical 
import bollingerx
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
import matplotlib as mpl

from pyalgotrade.technical import stats
#self.__stdDev = stats.StdDev(dataSeries, period, maxLen=maxLen)
#-----------
class BBands(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__bbands = bollingerx.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)

    def getBollingerBands(self):
        return self.__bbands

    
    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if lower is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        dprice=bar.getClose();
        dcash=self.getBroker().getCash(False) ;
        #dcash2=self.getBroker().getCash();
        
        css='$%.2f,$%.2f' % (lower,upper);
        css=css+',n,%d,$%.2f,$%.2f' %(shares,dprice,dcash)
        css=css+',@pos,'+str(self.getBroker().getPositions())
        if shares == 0 and dprice < lower:
            sharesToBuy = int(self.getBroker().getCash(False) / dprice)
            self.marketOrder(self.__instrument, sharesToBuy)
            s2='%d' % sharesToBuy
            dss=css+',nBuy,'+s2
            self.info('++ '+dss)
        elif shares > 0 and dprice> upper:
            self.marketOrder(self.__instrument, -1*shares)
            #self.info("-- $%.2f,$%.2f,$%.2f,$%.2f,$%.2f" % (lower,upper,shares,bar.getClose(),self.getBroker().getCash() ),self.getBroker().getPositions())
            self.info('-- '+css)


def main():
    instrument = "yhoo"
    bBandsPeriod = 40

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, "dat\\yhoo-201x.csv")

    strat = BBands(feed, instrument, bBandsPeriod)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    retAnalyzer = returns.Returns()
    strat.attachAnalyzer(retAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)
    
    #------
    mpl.style.use('seaborn-whitegrid');
    plt = plotter.StrategyPlotter(strat, True, True, True)
    plt.getInstrumentSubplot(instrument).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
    plt.getInstrumentSubplot(instrument).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
    plt.getInstrumentSubplot(instrument).addDataSeries("lower", strat.getBollingerBands().getLowerBand())

    strat.run()
    plt.plot()
    #==============================    
    print("最终资产价值 Final portfolio value: $%.2f" % strat.getResult())
    print("累计回报率 Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("夏普比率 Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
    print("最大回撤率 Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
    print("最长回撤时间 Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

        


#=========
main()
