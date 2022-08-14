from GuiPage.GuiPage import *

class TradingSystemInfoPage(GuiPage):
    def __init__(self,systemName):
        super(TradingSystemInfoPage,self).__init__()
        self.systemName = systemName

    def show(self,parent):
        super(TradingSystemInfoPage,self).show(parent)
