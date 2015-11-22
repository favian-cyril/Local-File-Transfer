from tkinter import *
from tkinter.filedialog import askdirectory

class Window(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Connect window
        self.geometry("500x250+30+30")
        self.label = Label(self, text='Please fill in below to access the application! \n')
        self.label.pack()
        
        Label(self, text="IP Address").pack()
        entry1 = Entry(self)
        entry1.pack()

        Label(self, text="Host").pack()
        entry2 = Entry(self)
        entry2.pack()

        # Continue to application main page
        self.wButton = Button(self, text='Connect', command = self.OnButtonClick)
        self.wButton.pack()

    def OnButtonClick(self):
        # Initialize 'Sync Kong' main window after user has connected
        self.top = Toplevel()
        self.top.title("Sync Kong")
        self.top.geometry("1200x500+30+30")
        self.top.transient(self)
        self.wButton.config(state='disabled')
        
        self.top.label = Label(self.top, text='You have connected. Have fun!')
        self.top.label.pack()
        
        # SyncKong's logo
        self.top.image = PhotoImage(file='gorilla.gif')
        Label(self.top, image=self.top.image).pack()

        # Sync Button
        self.refresh = Button(self.top, text="Sync with Kong!", command=self.refresh)
        self.refresh.pack()
        
        # Set Path Directory Button
        self.path = Button(self.top, text="Set Path", command=self.path)
        self.path.pack()
        
        # Back To Connect Button
        self.backButton = Button(self.top, text="Back To Connect", command = self.OnChildClose)
        self.backButton.pack()

    def OnChildClose(self):
        # Close and go back to 'Connect' state
        self.wButton.config(state='normal')
        self.top.destroy()

    def refresh(self):
        pass

    def path(self):
        # Get folder's directory
        self.filepath = askdirectory()
    
if __name__ == "__main__":
    window = Window(None)
    window.title("Connect To Sync Kong")
    window.mainloop()
