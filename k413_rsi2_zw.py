# -*- coding: utf-8 -*-
import rsi2
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import sharpe

import matplotlib as mpl
import pandas as pd
import zwQTBox as zwx

def main(plot):
    cod="002739";cname='wanda';csgn=u'万达院线'
    cod="600663";cname='lujiazui';csgn=u'陆家嘴'
    cod="600231";cname='lingang';csgn=u'凌钢股份'
    cod='002046';cname='zouyan';csgn=u'轴研科技'
    cod='300239';cname='donbao';csgn=u'东宝生物'
    
    fss="dat\\"+cod+".csv";
    df=pd.read_csv(fss,encoding='gbk');
    #df2=zwBox.zw_df2yhaoo(df);
    df2=zwx.df2yhaoo(df);
    cfn="dat\\"+cod+"_yh.csv";
    print csgn,cname,fss
    df2.to_csv(cfn,encoding='utf-8')
    #
    #instrument = "DIA"  #使用新变量名cname替代
    entrySMA = 200
    exitSMA = 5
    rsiPeriod = 2
    overBoughtThreshold = 90
    overSoldThreshold = 10

    # Download the bars.
    #feed = yahoofinance.build_feed([instrument], 2009, 2012, ".")
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(cname,cfn)

    strat = rsi2.RSI2(feed, cname, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        mpl.style.use('seaborn-whitegrid');
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(cname).addDataSeries("Entry SMA", strat.getEntrySMA())
        plt.getInstrumentSubplot(cname).addDataSeries("Exit SMA", strat.getExitSMA())
        plt.getOrCreateSubplot("rsi").addDataSeries("RSI", strat.getRSI())
        plt.getOrCreateSubplot("rsi").addLine("Overbought", overBoughtThreshold)
        plt.getOrCreateSubplot("rsi").addLine("Oversold", overSoldThreshold)

    strat.run()
    print "夏普指数 Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
