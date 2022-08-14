# 量化平台图形界面树
from ctypes import alignment
import PySimpleGUI as sg
import webbrowser

class guitree:
    def __init__(self, title, tree1, tree2, guipage = None):
        self.title = title
        self.tree1 = tree1
        self.tree2 = tree2
        self.guipage = guipage

    @staticmethod
    def elesize():
        return (20, 3)

    @staticmethod
    def elesize_icon():
        return (30, 30)

    @staticmethod
    def elesize_back():
        return (20, 1)

    @staticmethod
    def BTN(title):
        return sg.Button(
            title,
            size=guitree.elesize(),
            font=('楷体', 20)
        )

    @staticmethod
    def BTN_BACK(title):
        return sg.Button(
            title,
            size=guitree.elesize_back(),
            font=('楷体', 20)
        )

    @staticmethod
    def LAB(title):
        return sg.Button(
            title,
            size=guitree.elesize(),
            disabled=True,
            font=('楷体', 20)
        )

    @staticmethod
    def github():
        return guitree.center(sg.Image(
            # source="img\github_PNG40.png",
            source="img\github_PNG_60.png", #png图像调整www.iloveimg.com
            key="github",
            #background_color="black",
            visible=True,
            enable_events=True
            # size=guitree.elesize_icon()
        ))

    @staticmethod
    def center(ele):
        return sg.Column([[ele]], justification='center', vertical_alignment="center")

    def show(self, parent=None):
        self.parent = parent
        sg.theme('DarkAmber')   # Add a touch of color
        # sg.theme('DarkRed')   # Add a touch of color
        # sg.theme('Black')   # Add a touch of color
        # sg.theme('DarkBlack')   # Add a touch of color
        # All the stuff inside your window.
        if self.tree1:
            ele1 = guitree.BTN(self.tree1.title)
        else:
            ele1 = guitree.LAB("选项1：未定义")
        if self.tree2:
            ele2 = guitree.BTN(self.tree2.title)
        else:
            ele2 = guitree.LAB("选项2：未定义")
        github = guitree.github()
        if parent:
            parent_title = "<< 返回"
            ele0 = guitree.BTN_BACK(parent_title)
            layout = [
                [ele0],
                [ele1],
                [ele2],
                [github]
            ]
        else:
            parent_title = "<<"
            layout = [
                [ele1],
                [ele2],
                [github]
            ]

        # Create the Window
        window = sg.Window(self.title, layout, resizable=False, finalize=True)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if self.tree1 and event == self.tree1.title:
                window.close()
                self.tree1.show(self)
            elif self.tree2 and event == self.tree2.title:
                window.close()
                self.tree2.show(self)
            elif parent and event == parent_title:
                window.close()
                self.parent.show(self.parent.parent)
            elif event == 'github':
                webbrowser.open("https://github.com/trder/trder")