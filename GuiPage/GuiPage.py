#所有页面的基类
#所有页面都继承这个类，以确保风格的一致性
class GuiPage:
    def __init__(self):
        pass

    def show(self,parent):
        self.parent = parent

    def back(self):
        pass
