from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
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

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f,$%.2f,$%.2f" % (execInfo.getPrice(),self.__sma[-1],self.getBroker().getCash() ))
        #print('pos,',self.getBroker().getPositions())
        

    def onExitOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("Sell at $%.2f,$%.2f,$%.2f" % (execInfo.getPrice(),self.__sma[-1],self.getBroker().getCash() ))
        #
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        dcash=self.getBroker().getCash();dprice=bars[self.__instrument].getPrice();
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                
                shares = int( dcash* 0.9 / dprice)
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                #
                self.info("above: $%.2f,$%.2f,%.2f,%2d" % (dcash,dprice,self.__sma[-1],shares))
                print('pos,',self.getBroker().getPositions())
                print('')
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()
            #
            self.info("below: $%.2f,$%.2f,%.2f" % (dcash,dprice,self.__sma[-1] ))
            print('pos,',self.getBroker().getPositions())
            print('')