from GuiPage.GuiPage import *

#交易系统介绍页面，显示交易系统的介绍信息
class TradingSystemInfoPage(GuiPage):
    def __init__(self,systemName):
        super(TradingSystemInfoPage,self).__init__()
        self.systemName = systemName

    def show(self,parent):
        super(TradingSystemInfoPage,self).show(parent)
