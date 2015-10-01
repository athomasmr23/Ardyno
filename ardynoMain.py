import Tkinter as tk
#import matplotlib

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import Tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Ardyno(tk.Frame):
  
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Ardyno")
        
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        filemenu=tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Close")
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.destroy)
        menubar.add_cascade(label="File",menu=filemenu)

        commenu=tk.Menu(menubar, tearoff=0)
        commenu.add_command(label="Connect")
        menubar.add_cascade(label="Communications",menu=commenu)

        helpmenu=tk.Menu(menubar,tearoff=0)
        helpmenu.add_command(label="Help")
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help",menu=helpmenu)

        toolbar = tk.Frame(self.parent, bd=1, relief="raised")
        toolbar.pack(side="top", fill="x")

        testControlFrame = tk.Frame(self.parent, borderwidth=2,relief="groove")
        testControlFrame.pack(side="left", fill="both")

        #SAE Correction factor
        SAEcorrectionFrame = tk.LabelFrame(testControlFrame, borderwidth=2, relief="groove",text="SAE Correction")
        tk.Label(SAEcorrectionFrame,text="Ambient Temp [C]").grid(row=1,column=0,padx=5)
        tk.Label(SAEcorrectionFrame,relief="sunken",width=7).grid(row=2,column=0,padx=5,pady=5)
        tk.Label(SAEcorrectionFrame,text="Ambient Pressure [Kpa]").grid(row=3,column=0,padx=5)
        tk.Label(SAEcorrectionFrame,relief="sunken",width=7).grid(row=4,column=0,padx=5,pady=5)
        tk.Label(SAEcorrectionFrame,text="SAE Correction Factor").grid(row=5,column=0,padx=5)
        tk.Label(SAEcorrectionFrame,relief="sunken",width=7).grid(row=6,column=0,padx=5,pady=5)
        tk.Button(SAEcorrectionFrame,text="Correction Factor").grid(row=7,column=0,padx=5,pady=5,columnspan=2,rowspan=2)
        SAEcorrectionFrame.pack(side="top", fill="both")

        #Load cell setup and calibration
        LoadCellCal=tk.LabelFrame(testControlFrame,borderwidth=2,relief="groove",text="Calibration")
        tk.Label(LoadCellCal,text="No Load").grid(row=3,column=0,padx=5)
        tk.Label(LoadCellCal,relief="sunken",width=6).grid(row=3,column=1,padx=5,pady=5)
        tk.Label(LoadCellCal,text="Loaded").grid(row=4,column=0,padx=10)
        tk.Label(LoadCellCal,relief="sunken",width=6).grid(row=4,column=1,padx=5,pady=5)
        tk.Button(LoadCellCal,text="Unloaded Calibration").grid(row=3,column=2,padx=5,pady=5,columnspan=1,rowspan=1)
        tk.Button(LoadCellCal,text="Loaded Calibration").grid(row=4,column=2,padx=5,pady=5,columnspan=1,rowspan=1)

        tk.Label(LoadCellCal,text="Calibration distance [in]").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        entryL=tk.Entry(LoadCellCal,width=6)
        entryL.grid(row=0,column=1,padx=5,pady=5,columnspan=2,sticky="w")
        entryL.delete(0,"end")
        entryL.insert(0,4.75)

        tk.Label(LoadCellCal,text="Calibration weight [lbf]").grid(row=1,column=0,padx=5,pady=5,sticky="w")
        entryW=tk.Entry(LoadCellCal,width=6)
        entryW.grid(row=1,column=1,padx=5,pady=5,columnspan=2,sticky="w")
        entryW.delete(0,"end")
        entryW.insert(0,10.08)

        tk.Label(LoadCellCal,relief="sunken",width=40).grid(row=5,column=0,padx=5,pady=5,columnspan=3,sticky="e")
        tk.Button(LoadCellCal,text="Generate Fit").grid(row=5,column=3,padx=5,pady=5,rowspan=1)

        LoadCellCal.pack(fill="both")

        testOperationFrame = tk.Frame(self.parent, borderwidth=2,relief="groove")
        testOperationFrame.pack(side="right", fill="both")
        RunStopFrame=tk.LabelFrame(testOperationFrame,borderwidth=2,relief="groove")
        tk.Button(RunStopFrame,text="Create Test").grid(row=0,column=0,padx=5,pady=5,columnspan=2)
        tk.Button(RunStopFrame,text="Run").grid(row=1,column=0,padx=5,pady=5)
        tk.Button(RunStopFrame,text="Stop").grid(row=1,column=1,padx=5,pady=5)
        tk.Button(RunStopFrame,text="Plot").grid(row=2,column=0,padx=5,pady=5)
        tk.Button(RunStopFrame,text="Export").grid(row=2,column=1,padx=5,pady=5,columnspan=2)
        RunStopFrame.pack(padx=10,pady=10)
      
##        fig=plt.Figure()
##        graphCanvas = FigureCanvasTkAgg(fig, self.parent)
##        graphCanvas.get_tk_widget().grid(column=0,row=0)
        #graphCanvas.pack(side=TOP, fill=BOTH)

        self.parent.config(menu=menubar)
        self.pack()
                

    def onExit(self):
        self.quit()


def main():
  
    root = tk.Tk()
    root.geometry("917x540+300+300")
    app = Ardyno(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
