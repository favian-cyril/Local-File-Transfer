from tkinter import *

class Window(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Connect window
        self.geometry("300x150+30+30")
        self.wButton = Button(self, text='Connect', command = self.OnButtonClick)
        self.wButton.pack()

    def OnButtonClick(self):
        # Initialize 'Sync Kong' main window after user has connected
        self.top = Toplevel()
        self.top.title("Sync Kong")
        self.top.geometry("600x400+30+30")
        self.top.transient(self)
        self.wButton.config(state='disabled')
        self.topButton = Button(self.top, text="CLOSE", command = self.OnChildClose)
        self.topButton.pack()

    def OnChildClose(self):
        # Close and go back to 'Connect' state
        self.wButton.config(state='normal')
        self.top.destroy()

if __name__ == "__main__":
    window = Window(None)
    window.title("Connect To Sync Kong")
    window.mainloop()
