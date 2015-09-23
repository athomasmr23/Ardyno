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

        #SAE Correction factor
        SAEcorrectionFrame = LabelFrame(testControlFrame, borderwidth=2, relief=GROOVE,text="SAE Correction")
        Label(SAEcorrectionFrame,text="Ambient Temp [C]").grid(row=1,column=0,padx=5)
        Label(SAEcorrectionFrame,relief=SUNKEN,width=7).grid(row=2,column=0,padx=5,pady=5)
        Label(SAEcorrectionFrame,text="Ambient Pressure [Kpa]").grid(row=3,column=0,padx=5)
        Label(SAEcorrectionFrame,relief=SUNKEN,width=7).grid(row=4,column=0,padx=5,pady=5)
        Label(SAEcorrectionFrame,text="SAE Correction Factor").grid(row=5,column=0,padx=5)
        Label(SAEcorrectionFrame,relief=SUNKEN,width=7).grid(row=6,column=0,padx=5,pady=5)
        Button(SAEcorrectionFrame,text="Correction Factor").grid(row=7,column=0,padx=5,pady=5,columnspan=2,rowspan=2)
        SAEcorrectionFrame.pack(side=TOP, fill=BOTH)

        #Load cell setup and calibration
        LoadCellCal=LabelFrame(testControlFrame,borderwidth=2,relief=GROOVE,text="Calibration")
        Label(LoadCellCal,text="No Load").grid(row=3,column=0,padx=5)
        Label(LoadCellCal,relief=SUNKEN,width=6).grid(row=3,column=1,padx=5,pady=5)
        Label(LoadCellCal,text="Loaded").grid(row=4,column=0,padx=10)
        Label(LoadCellCal,relief=SUNKEN,width=6).grid(row=4,column=1,padx=5,pady=5)
        Button(LoadCellCal,text="Unloaded Calibration").grid(row=3,column=2,padx=5,pady=5,columnspan=1,rowspan=1)
        Button(LoadCellCal,text="Loaded Calibration").grid(row=4,column=2,padx=5,pady=5,columnspan=1,rowspan=1)

        Label(LoadCellCal,text="Calibration distance [in]").grid(row=0,column=0,padx=5,pady=5,sticky=W)
        entryL=Entry(LoadCellCal,width=6)
        entryL.grid(row=0,column=1,padx=5,pady=5,columnspan=2,sticky=W)
        entryL.delete(0,END)
        entryL.insert(0,4.75)

        Label(LoadCellCal,text="Calibration weight [lbf]").grid(row=1,column=0,padx=5,pady=5,sticky=W)
        entryW=Entry(LoadCellCal,width=6)
        entryW.grid(row=1,column=1,padx=5,pady=5,columnspan=2,sticky=W)
        entryW.delete(0,END)
        entryW.insert(0,10.08)

        Label(LoadCellCal,relief=SUNKEN,width=40).grid(row=5,column=0,padx=5,pady=5,columnspan=3,sticky=E)
        Button(LoadCellCal,text="Generate Fit").grid(row=5,column=3,padx=5,pady=5,rowspan=1)

        LoadCellCal.pack(fill=BOTH)

        testOperationFrame = Frame(self.parent, borderwidth=2,relief=GROOVE)
        testOperationFrame.pack(side=RIGHT, fill=BOTH)
        RunStopFrame=LabelFrame(testOperationFrame,borderwidth=2,relief=GROOVE)
        Button(RunStopFrame,text="Create Test").grid(row=0,column=0,padx=5,pady=5,columnspan=2)
        Button(RunStopFrame,text="Run").grid(row=1,column=0,padx=5,pady=5)
        Button(RunStopFrame,text="Stop").grid(row=1,column=1,padx=5,pady=5)
        Button(RunStopFrame,text="Plot").grid(row=2,column=0,padx=5,pady=5)
        Button(RunStopFrame,text="Export").grid(row=2,column=1,padx=5,pady=5,columnspan=2)
        RunStopFrame.pack(padx=10,pady=10)
      

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
