from Tkinter import *

class Ardyno(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Ardyno")
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        filemenu=Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Close")
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.destroy)
        menubar.add_cascade(label="File",menu=filemenu)

        commenu=Menu(menubar, tearoff=0)
        commenu.add_command(label="Connect")
        menubar.add_cascade(label="Communications",menu=commenu)

        helpmenu=Menu(menubar,tearoff=0)
        helpmenu.add_command(label="Help")
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help",menu=helpmenu)

        toolbar = Frame(self.parent, bd=1, relief=RAISED)
        toolbar.pack(side=TOP, fill=X)

        testControlFrame = Frame(self.parent, borderwidth=2,relief=GROOVE)
        testControlFrame.pack(side=LEFT, fill=BOTH)

        SAEcorrectionFrame = Frame(testControlFrame, borderwidth=2, relief=GROOVE)
        Label(SAEcorrectionFrame,text="Ambient Temp [C]").grid(row=1,column=0,padx=5)
        Label(SAEcorrectionFrame,relief=SUNKEN,width=7).grid(row=2,column=0,padx=5,pady=5)
        Label(SAEcorrectionFrame,text="Ambient Pressure [Kpa]").grid(row=3,column=0,padx=5)
        Label(SAEcorrectionFrame,relief=SUNKEN,width=7).grid(row=4,column=0,padx=5,pady=5)
        Label(SAEcorrectionFrame,text="SAE Correction Factor").grid(row=5,column=0,padx=5)
        Label(SAEcorrectionFrame,relief=SUNKEN,width=7).grid(row=6,column=0,padx=5,pady=5)
        Button(SAEcorrectionFrame,text="Correction Factor").grid(row=7,column=0,padx=5,pady=5,columnspan=2,rowspan=2)
        SAEcorrectionFrame.pack(side=TOP, fill=BOTH)
      

        graphCanvas = Canvas(self.parent)
        graphCanvas.pack(side=TOP, fill=BOTH)

        

        self.parent.config(menu=menubar)
        self.pack()
                

    def onExit(self):
        self.quit()


def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Ardyno(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
