import webbrowser
from GuiPage.GuiPage import *
import PySimpleGUI as sg

# 默认页面（当页面未实现时，调用默认页面）
class DefaultPage(GuiPage):
    def __init__(self, title="Title"):
        super(DefaultPage, self).__init__(title)

    def show(self, parent):
        super(DefaultPage, self).show(parent)
        textarea = GuiPage.center(sg.Text(
            text="此处施工中，敬请期待！",
            size=(20, 5),
            font=('楷体', 20)
        )
        )

        github = GuiPage.github()
        if parent:
            parent_title = "<< 返回"
            ele0 = GuiPage.BTN_BACK(parent_title)
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
