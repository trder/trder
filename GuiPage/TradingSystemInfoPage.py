from GuiPage.GuiPage import *

#交易系统介绍页面，显示交易系统的介绍信息
class TradingSystemInfoPage(GuiPage):
    def __init__(self,tradingsystem,tradingsystemInfo,title="Title"):
        super(TradingSystemInfoPage,self).__init__(title)
        self.tradingsystem = tradingsystem
        self.tradingsystemInfo = tradingsystemInfo

    def show(self,parent):
        super(TradingSystemInfoPage, self).show(parent)
        textarea = GuiPage.center(sg.Text(
            text=self.tradingsystem+"简介:\n\n"+self.tradingsystemInfo,
            size=(40, 13),
            font=('楷体', 20)
        )
        )

        github = GuiPage.github()
        if parent:
            parent_title = "<< 返回"
            ele0 = sg.Button(
                parent_title,
                size=(40, 1),
                font=('楷体', 20)
            )
            layout = [
                [ele0],
                [textarea],
                [github]
            ]
        else:
            parent_title = "<<"
            layout = [
                [textarea],
                [github]
            ]
        # Create the Window
        window = sg.Window(self.title, layout, resizable=False, finalize=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif parent and event == parent_title:
                window.close()
                self.parent.show(self.parent.parent)
            elif event == 'github':
                GuiPage.navi_github()
