# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import bollinger
from pyalgotrade.stratanalyzer import sharpe

import matplotlib as mpl
import pandas as pd
import zwQTBox as zwx


class BBands(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)

    def getBollingerBands(self):
        return self.__bbands

    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if lower is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        if shares == 0 and bar.getClose() < lower:
            sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose())
            self.marketOrder(self.__instrument, sharesToBuy)
        elif shares > 0 and bar.getClose() > upper:
            self.marketOrder(self.__instrument, -1*shares)


def main(plot):
    cod="002739";#万达院线
    cname='wanda';
    fss="dat\\"+cod+".csv";
    df=pd.read_csv(fss,encoding='gbk');
    #df2=zwBox.zw_df2yhaoo(df);
    df2=zwx.df2yhaoo(df);
    cfn="dat\\"+cod+"_yh.csv";print(fss);
    df2.to_csv(cfn,encoding='utf-8')
    #
    #instrument = "yhoo" #使用新变量名cname替代
    #bBandsPeriod = 40
    bBandsPeriod = 10

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(cname,cfn)

    strat = BBands(feed, cname, bBandsPeriod)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        mpl.style.use('seaborn-whitegrid');
        plt = plotter.StrategyPlotter(strat, True, True, True)
        plt.getInstrumentSubplot(cname).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        plt.getInstrumentSubplot(cname).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        plt.getInstrumentSubplot(cname).addDataSeries("lower", strat.getBollingerBands().getLowerBand())

    strat.run()
    print( "夏普指数 Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

    if plot:
        plt.plot()
        
        
    
if __name__ == "__main__":
    
    main(True)
