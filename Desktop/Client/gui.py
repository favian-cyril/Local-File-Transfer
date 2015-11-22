from tkinter import *
from tkinter.filedialog import askopenfilename

class UploadButton(Button):
    def __init__(self, parent=None, side=TOP, **config): 
        Button.__init__(self, parent, config)            
        self.pack(side=side)                             
        self.config(command=self.callback)

    def callback(self):
        self.upload = askopenfilename()
 
if __name__ == '__main__':
    root = Tk()
    root.title("Sync Kong")
    root.geometry("300x300")
    UploadButton(side=TOP, text='Upload Files').mainloop()
    UploadButton.center()
