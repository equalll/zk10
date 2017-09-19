# -*- coding: utf-8 -*-
import sma_crossover
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe
import pandas as pd
import zwQTBox as zwx


def main(plot):
    #--------数据格式转换，常用国内A股数据，转换为yahoo财经格式
    cod="002739";#万达院线
    cname='wanda';
    fss="dat\\"+cod+".csv";
    df=pd.read_csv(fss,encoding='gbk');
    df2=zwx.df2yhaoo(df);
    cfn="dat\\"+cod+"_yh.csv";print(fss);
    df2.to_csv(cfn,encoding='utf-8')
    #------------
    #instrument = "aapl",使用新变量名cname替代
    #smaPeriod = 163
    smaPeriod = 20

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2011, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(cname,cfn)


    strat = sma_crossover.SMACrossOver(feed,cname, smaPeriod)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(cname).addDataSeries("sma", strat.getSMA())

    strat.run()
    print "夏普指数 Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
