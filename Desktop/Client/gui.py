from tkinter import *
from tkinter.filedialog import askdirectory

class Window(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Connect window
        self.geometry("500x350+30+30")
        # SyncKong's logo
        self.image = PhotoImage(file='assets/welcome.gif')
        Label(self, image=self.image).pack()

        # Connect form
        Label(self, text="IP Address").pack()
        entry1 = Entry(self)
        entry1.pack()
        Label(self, text="Host").pack()
        entry2 = Entry(self)
        entry2.pack()
        Label(self, text="").pack()

        # Set Path Directory Button
        self.path = Button(self, text="Set Path", command=self.path, width=18)
        self.path.pack()
        self.filepath = 'Data/'
        self.pathname = Label(self,text="Current path: {}".format(self.filepath))
        self.pathname.pack()
        Label(self, text="").pack()

        # Process to SyncKong app
        self.wButton = Button(self, text='Connect', command =self.OnButtonClick)
        self.wButton.pack()

        # Exception: if IP address & Host fill is wrong, alert user

    def OnButtonClick(self):
        # Initialize 'Sync Kong' main window after user has connected
        self.top = Toplevel()
        self.top.title("Sync Kong")
        self.top.geometry("700x400+30+30")
        self.top.transient(self)
        self.wButton.config(state='disabled')
        
        # SyncKong's logo
        self.top.image = PhotoImage(file='assets/gorilla.gif')
        Label(self.top, image=self.top.image).pack()

        # Sync Button
        self.refresh = Button(self.top, text="Sync with Kong!", command=self.refresh)
        self.refresh.pack()
        
        # Back To Connect Button
        self.backButton = Button(self.top, text="Back To Connect", command=self.OnChildClose)
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
        self.pathname['text'] = "Current path: {}".format(self.filepath)

    def warning(self):
        # User get popup notification if auth is failed
        self.warning = messagebox.showerror("Cannot connect to server", "Configuration error, please try again!")
        
if __name__ == "__main__":
    window = Window(None)
    window.title("Connect To Sync Kong")
    window.mainloop()
