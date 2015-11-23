from tkinter import *
from tkinter.filedialog import askdirectory
import client
from threading import Thread
import queue

class SyncThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)

    def run():
        client.run()

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
        self.entry1 = Entry(self)
        self.entry1.pack()
        Label(self, text="Host").pack()
        self.entry2 = Entry(self)
        self.entry2.pack()
        Label(self, text="").pack()

        # Set Path Directory Button
        self.path = Button(self, text="Set Path", command=self.path, width=18)
        self.path.pack()
        self.filepath = 'Data\\'
        self.pathname = Label(self,text="Current path: {}".format(self.filepath))
        self.pathname.pack()
        Label(self, text="").pack()
        

        # Process to SyncKong app
        self.wButton = Button(self, text='Connect', command =self.connect)
        self.wButton.pack()

        # Exception: if IP address & Host fill is wrong, alert user
    def connect(self):
        client.setIP(self.entry1.get())    
        client.setPort(int(self.entry2.get()))
        client.setPath(self.filepath)
        try:
            client.connect()
        except:
            self.warning()
        else:
            client.run()
            self.OnButtonClick()

        
        
    
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
        self.backButton = Button(self.top, text="Disconnect", command=self.OnChildClose)
        self.backButton.pack()
        
        self.lastupdate = Label(self.top, text='Latest Update: {}'.format(client.lastUpdate()))
        self.lastupdate.pack()
        self.lastUpdate()


    def OnChildClose(self):
        # Close and go back to 'Connect' state
        client.closeConnection()
        self.wButton.config(state='normal')
        self.top.destroy()

    def refresh(self):
        client.checkWithServer()

    def path(self):
        # Get folder's directory
        self.filepath = askdirectory()
        self.pathname['text'] = "Current path: {}".format(self.filepath)

    def warning(self):
        # User get popup notification if auth is failed
        self.warning = messagebox.showerror("Cannot connect to server", "Configuration error, please try again!")

    def lastUpdate(self):
        self.lastupdate['text'] = 'Latest Update: {}'.format(client.lastUpdate())
        self.after(6000,self.lastUpdate)                                                    

if __name__ == "__main__":
    window = Window(None)
    window.title("Connect To Sync Kong")
    window.mainloop()


