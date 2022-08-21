import webbrowser
import PySimpleGUI as sg

#所有页面的基类
#所有页面都继承这个类，以确保风格的一致性
class GuiPage:
    def __init__(self,title="Title"):
        self.title = title

    def show(self,parent):
        self.parent = parent
        sg.theme('DarkAmber')   # Add a touch of color

    def back(self):
        pass
    
    @staticmethod
    def center(ele):
        return sg.Column([[ele]], justification='center', vertical_alignment="center")

    @staticmethod
    def github():
        return GuiPage.center(sg.Image(
            # source="img\github_PNG40.png",
            source="img\github_PNG_60.png", #png图像调整www.iloveimg.com
            key="github",
            #background_color="black",
            visible=True,
            enable_events=True
            # size=guitree.elesize_icon()
        ))

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
    def BTN_BACK(title):
        return sg.Button(
            title,
            size=GuiPage.elesize_back(),
            font=('楷体', 20)
        )
        
    @staticmethod
    def navi_github():
        webbrowser.open("https://github.com/trder/trder")