#量化平台图形界面树
from ctypes import alignment
import PySimpleGUI as sg

class guitree:
    def __init__(self,title,tree1,tree2):
        self.title = title
        self.tree1 = tree1
        self.tree2 = tree2

    @staticmethod
    def elesize():
        return (30,4)

    @staticmethod
    def BTN(title):
        return sg.Button(title,size=guitree.elesize()) 

    @staticmethod
    def LAB(title):
        return sg.Text(title,size=guitree.elesize(),justification='center') 

    def show(self):
        sg.theme('DarkAmber')   # Add a touch of color
        # All the stuff inside your window.
        if self.tree1:
            ele1 = guitree.BTN(self.tree1.title)
        else:
            ele1 = guitree.LAB("选项1：未定义")
        if self.tree2:
            ele2 = guitree.BTN(self.tree2.title)
        else:
            ele2 = guitree.LAB("选项2：未定义")
        layout = [  [ele1],
                    [ele2] ]

        # Create the Window
        window = sg.Window(self.title, layout, resizable=True, finalize=True)

        while True:
            event,values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if self.tree1 and event == self.tree1.title:
                self.tree1.show()
            elif self.tree2 and event == self.tree2.title:
                self.tree2.show()

        window.close()