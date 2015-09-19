from Tkinter import *
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

import serial
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import tkMessageBox

# Serial port parameters
serial_speed = 1000000
serial_port = '/dev/ttyACM0'

def correction():
    #Request data from arduino and read
    try:
        ser.write('t')
    except NameError:
        tkMessageBox.showerror("Error","No serial connection found!")
        return
    
    datat=ser.readline()

    try:
        ser.write('p')
    except NameError:
        tkMessageBox.showerror("Error","No serial connection found!")
        return
    
    datap=ser.readline()

    #Break incoming data into the P and C vars
    if (datat != "" and datap !=""):
        processed_datat = datat.split(",")
        processed_datap = datap.split(",")

        temp = [float(list_item) for list_item in processed_datat]
        press = [float(list_item) for list_item in processed_datap]
        atmPressKpa = np.mean(press)
        atmTempC = np.mean(temp)

    CF = 1.176*((99.0/(atmPressKpa-1))*math.sqrt(((atmTempC+273.0)/298.0)))-.176
    CFlbl.set(round(CF,3))
    atmPressKpalbl.set(round(atmPressKpa,3))
    atmTempClbl.set(round(atmTempC,3))

def calibrationNL():
    try:
        ser.write('s')
    except NameError:
        tkMessageBox.showerror("Error","No serial connection found!")
        return

    data=ser.readline()

    if(data != ""):
        processed_data=data.split(",")
        cal = [long(list_item) for list_item in processed_data]
        calAvg = np.mean(cal)
    calAvgNLlbl.set(round(calAvg,1))

def calibrationL():
    try:
        ser.write('s')
    except NameError:
        tkMessageBox.showerror("Error","No serial connection found!")
        return
    
    data=ser.readline()

    if(data != ""):
        processed_data=data.split(",")
        cal = [long(list_item) for list_item in processed_data]
        calAvg = np.mean(cal)
    calAvgLlbl.set(round(calAvg,1))

def ADCconversion():
    inches=calLenght.get()
    ft=inches/12.0
    lbs=calWeight.get()
    x=np.array([calAvgNLlbl.get(),calAvgLlbl.get()])
    y=np.array([0,(ft*lbs)])
    A=np.vstack([x,np.ones(len(x))]).T
    m,c=np.linalg.lstsq(A,y)[0]
    calSlope.set(round(m,5))
    calIntercept.set(round(c,5))
    calEquation.set("Torque = {0:.5E} * ADC + {1:.5E}".format(m,c))

def readVal():
    m=calSlope.get()
    b=calIntercept.get()
    injFlow = 44.1 #cc/min flow
    fuelDen = 0.69192 #g/cc isooctane
    injDeadTime = 161 #injector deadtime in microseconds get from TunerStudio
    CF = CFlbl.get()
    
    #Request data from arduino
    try:
        ser.write('r')
    except NameError:
        tkMessageBox.showerror("Error","No serial connection found!")
        return
    
    data=ser.readline()

    if (data != ""):
        processed_data = data.split(",")

        timePulse=long(processed_data[0])
        mapRaw=int(processed_data[1])
        injPulse=long(processed_data[2])
        torqueRaw=long(processed_data[3])

    try:
        rpmVal = round(1000000.0*(2*math.pi/6.0)/timePulse*(30.0/math.pi)) #6 is the number of pucks
    except ZeroDivisionError:
        tkMessageBox.showerror("Error","RPM timePulse=0; divide by 0 error")
    mapVal = 0.091 * mapRaw + 9.0766
    injPulse = (injPulse - injDeadTime)/(60000000.0) #inj time in minutes
    fuelConsumption = (injPulse*injFlow)*(rpmVal/2)*fuelDen*60 #g/hr
    torqueVal = CF*(m * torqueRaw + b)
    kW = (1.3558179483314*torqueVal)*(rpmVal*(math.pi/30))/1000
    try:
        bsfcVal = fuelConsumption/kW #g/kW-hr
    except ZeroDivisionError:
        tkMessageBox.showerror("Error","BSFC Error: check strain gauge calibration")
    if (bsfcVal < 0 or bsfcVal > 3000):
        bsfcVal=0
        
    return mapVal, rpmVal, torqueVal, bsfcVal   

def CreateLogger():
    MAP=np.linspace(1,101,num=101)
    rpm=np.linspace(500,5100,num=101)
    count=[[0 for y in range(len(MAP))] for x in range(len(rpm))]
    torque=[[0 for y in range(len(MAP))] for x in range(len(rpm))]
    bsfc=[[0 for y in range(len(MAP))] for x in range(len(rpm))]
    
def RunLogger():
    def record():
        mapVal,rpmVal,torqueVal, bsfcVal = readVal()
        interval=30000/rpmVal
        x=np.digitize([rpmVal],rpm)
        y=np.digitize([mapVal],MAP)

        try:
            count[y][x]=count[y][x]+1
            torque[y][x]=((count[y][x]-1)*torque[y][x]+torqueVal)/count[y][x]
            bsfc[y][x]=((count[y][x]-1)*bsfc[y][x]+bsfcVal)/count[y][x]
            #print count[y][x],torque[y][x],bsfc[y][x]
            #print mapVal,rpmVal,torqueVal,bsfcVal
            #print y,x
        except IndexError:
            print "Out of range data not recorded"
            pass
        root._job=root.after(int(interval),record)
    try:
        root._job=root.after(5,record)
    except NameError:
        tkMessageBox.showerror("Error","No serial connection found!")
        
def StopLogger():
    if root._job is not None:
        root.after_cancel(root._job)
        root._job=None

def PlotLogger():
    fig=plt.figure()
    X=rpm
    Y=MAP
    X,Y = np.meshgrid(X,Y)
    Z0=count
    Z1=torque
    Z2=bsfc
    try:
        contourf=plt.contourf(X,Y,Z0,alpha=.95,levels=range(0,750,25)) #range setting provide .95CI at +/-0.05
    except:
        tkMessageBox.showerror("Error","There is no data to plot!")
    try:
        cb=fig.colorbar(contourf, shrink=0.5, aspect=5)
        cb.set_label('count')
        plt.xlabel('RPM')
        plt.ylabel('MAP [Kpa]')
        plt.show()
    except:
        pass
    

def SaveLogger():
    np.savetxt("MAPaxis.csv",MAP,fmt='%3.1f',delimiter=",")
    np.savetxt("rpmAxis.csv",rpm,fmt='%4.1f',delimiter=",")
    np.savetxt("count.csv",count,fmt='%6.0f',delimiter=",")
    np.savetxt("torque.csv",torque,fmt='%2.5f',delimiter=",")
    np.savetxt("bsfc.csv",bsfc,fmt='%5.2f',delimiter=",")

def About():
    tkMessageBox.showinfo("About","Rowan Supermilage ArDyno\nVersion: 0.1b\nBy: Aaron Thomas")

def Connect():
    try:
        ser = serial.Serial(serial_port,serial_speed,timeout=5)
    except:# serial.SerialException:
        tkMessageBox.showwarning("Warning!","No connection to the device could be established")
        #pass

##############################################################################     
#   GUI INTERFACE
##############################################################################    
root=Tk()

try:
    ser = serial.Serial(serial_port,serial_speed,timeout=5)
except:# serial.SerialException:
    tkMessageBox.showwarning("Warning!","No connection to the device could be established")
    #pass


#Global variables
root._job=None
MAP=np.linspace(2,102,num=101)
rpm=np.linspace(500,5100,num=101)
count=[[0 for y in range(len(MAP))] for x in range(len(rpm))]
torque=[[0 for y in range(len(MAP))] for x in range(len(rpm))]
bsfc=[[0 for y in range(len(MAP))] for x in range(len(rpm))]

#Variables for GUI use
atmTempClbl=DoubleVar()
atmTempClbl.set(25.000)
atmPressKpalbl=DoubleVar()
atmPressKpalbl.set(101.325)
CFlbl=DoubleVar()
CFlbl.set(1.000)
calAvgNLlbl=DoubleVar()
calAvgLlbl=DoubleVar()
calLenght=DoubleVar()
calWeight=DoubleVar()
calSlope=DoubleVar()
calIntercept=DoubleVar()
calEquation=StringVar()

#SAE Correction factor frame
frame1=Frame(root,borderwidth=2,relief=GROOVE)
frame1.pack(padx=10,pady=10)
Label(frame1,text="Ambient Temp [C]").grid(row=1,column=0,padx=5)
Label(frame1,textvariable=atmTempClbl,relief=SUNKEN,width=7).grid(row=2,column=0,padx=5,pady=5)
Label(frame1,text="Ambient Pressure [Kpa]").grid(row=1,column=1,padx=5)
Label(frame1,textvariable=atmPressKpalbl,relief=SUNKEN,width=7).grid(row=2,column=1,padx=5,pady=5)
Label(frame1,text="SAE Correction Factor").grid(row=1,column=2,padx=5)
Label(frame1,textvariable=CFlbl,relief=SUNKEN,width=7).grid(row=2,column=2,padx=5,pady=5)
Button(frame1,text="Correction Factor",command=correction).grid(row=1,column=3,padx=5,pady=5,columnspan=2,rowspan=2)

#Load cell setup/calibration frame
frame2=Frame(root,borderwidth=2,relief=GROOVE)
frame2.pack(padx=10,pady=10)
Label(frame2,text="No Load").grid(row=1,column=0,padx=10)
Label(frame2,textvariable=calAvgNLlbl,relief=SUNKEN,width=6).grid(row=2,column=0,padx=10,pady=5)
Label(frame2,text="Loaded").grid(row=1,column=3,padx=10)
Label(frame2,textvariable=calAvgLlbl,relief=SUNKEN,width=6).grid(row=2,column=3,padx=10,pady=5)
Button(frame2,text="Unloaded Calibration",command=calibrationNL).grid(row=1,column=1,padx=5,pady=5,columnspan=2,rowspan=2)
Button(frame2,text="Loaded Calibration",command=calibrationL).grid(row=1,column=4,padx=5,pady=5,columnspan=2,rowspan=2)
Label(frame2,text="Calibration distance [in]").grid(row=0,column=0,padx=5,pady=5,sticky=W)

entryL=Entry(frame2,textvariable=calLenght,width=6)
entryL.grid(row=0,column=1,padx=5,pady=5,columnspan=2,sticky=W)
entryL.delete(0,END)
entryL.insert(0,4.75)

Label(frame2,text="Calibration weight [lbf]").grid(row=0,column=3,padx=5,pady=5,sticky=W)

entryW=Entry(frame2,textvariable=calWeight,width=6)
entryW.grid(row=0,column=4,padx=5,pady=5,columnspan=2,sticky=W)
entryW.delete(0,END)
entryW.insert(0,10.08)

Label(frame2,textvariable=calEquation,relief=SUNKEN,width=40).grid(row=3,column=0,padx=10,pady=5,columnspan=3,sticky=E)
Button(frame2,text="Generate Fit",command=ADCconversion).grid(row=3,column=3,padx=5,pady=5,rowspan=2)

#Testing frame
frame3=Frame(root,borderwidth=2,relief=GROOVE)
frame3.pack(padx=10,pady=10)
#Button(frame3,text="Create Test",command=CreateLogger).grid(row=0,column=0,padx=5,pady=5)
Button(frame3,text="Run",command=RunLogger).grid(row=0,column=2,padx=5,pady=5)
Button(frame3,text="Stop",command=StopLogger).grid(row=0,column=3,padx=5,pady=5)
Button(frame3,text="Plot",command=PlotLogger).grid(row=0,column=0,padx=5,pady=5)
Button(frame3,text="Export",command=SaveLogger).grid(row=0,column=1,padx=5,pady=5)
       

#Root window features
menubar=Menu(root)
filemenu=Menu(menubar, tearoff=0)
filemenu.add_command(label="New",command=CreateLogger)
filemenu.add_command(label="Open")
filemenu.add_command(label="Save",command=SaveLogger)
filemenu.add_command(label="Save as...")
filemenu.add_command(label="Close")
filemenu.add_separator()
filemenu.add_command(label="Exit",command=root.destroy)
menubar.add_cascade(label="File",menu=filemenu)

commenu=Menu(menubar, tearoff=0)
commenu.add_command(label="Connect",command=Connect)
menubar.add_cascade(label="Communications",menu=commenu)

helpmenu=Menu(menubar,tearoff=0)
helpmenu.add_command(label="About",command=About)
menubar.add_cascade(label="Help",menu=helpmenu)

#Root window buttons
Button(root,text="Exit",command=root.destroy).pack(padx=10,pady=10)

#Start window
root.config(menu=menubar)
root.title('Ardyno')
root.mainloop()
