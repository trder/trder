from GuiPage.GuiPage import *

#默认页面（当页面未实现时，调用默认页面）
class DefaultPage(GuiPage):
    def __init__(self):
        super(DefaultPage,self).__init__()

    def show(self,parent):
        super(DefaultPage,self).show(parent)
