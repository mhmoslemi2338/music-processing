from Music import *
import sounddevice as sd
import tkinter as tk
from tkinter import ttk

rawnotes=[]#each note is 50ms
freqq=[]
domainn=[]
T=0.05

def execute():
    fs1,data1=Music.read_mp3(root.filedir)     
    interval=int(fs1*T)
    oo=len(data1)
    oo=int(oo*0.3)
    DATA=data1[:,0]
    delta_t=vol.get()
    k=int((delta_t/50)*interval)
    
    for i in range(0,len(data1)-1*interval,interval):
        DATA[i:i+interval]=data1[i:i+interval,0]
        for j in range(1,6):
            try:
                DATA[i:i+interval]=DATA[i:i+interval]+((0.33)**j)*((-1)**j)*data1[i-k*j:i+interval-k*j,0]
            except:
                pass
    root.DATA=DATA
    root.interval=interval
    root.fs1=fs1
    lbl.configure(text='Done!',font='Helvetica 12 bold')
  
    

########################## --- GUI --- ######################################

root=tk.Tk()
#variables
root.title('Chorus')
root.play,root.fs1,root.interval,root.tmp,root.ply=0,0,0,0,0
root.outdst,root.filedir,root.name,root.name2='','','',''
root.DATA=[]
scale_var = tk.DoubleVar()
scale_var.set(50)
#labels
lbl=tk.Label(root, text="",font='Helvetica 12 bold')
tk.Label(root,text='\ndelta t (ms) Chorus:',font='Helvetica 12').grid(row=1,padx=4,pady=10,column=0)
lbl.grid(row=0,column=1,pady=5,padx=5)
#volume bars
vol = tk.Scale(root,from_ = 0,to = 1000,orient = tk.HORIZONTAL ,resolution = 25,variable=scale_var,length=250)
vol.grid(row=1,pady=0,padx=4,column=1)
#buttons
tk.Button(root, text="import/apply",font='bold',width=15,command=lambda:importt()).grid(pady=10,padx=20,row=2,column=0)
tk.Button(root, text="play/stop",font='bold',width=15,command=lambda:playy()).grid(padx=10,pady=20,row=2,column=1)
tk.Button(root, text="save",font='bold',width=15,command=lambda:savee()).grid(padx=1,pady=10,row=7,column=1)
tk.Button(root, text="Back",font='bold', command=lambda:root.destroy(),width=15).grid(pady=5,padx=1,row=7,column=0)


#functions
def savee():
    if root.filedir!='':
        if root.tmp!=vol.get():
            lbl.configure(text='just a sec!',font='Helvetica 12 bold')
            root.update_idletasks()
            execute()
        root.outdst=tkinter.filedialog.askdirectory(parent=root,title='choose music')
        root.outdst=str(root.outdst)+'/'+root.name+'_{} ms Chorus.mp3'.format(vol.get())
        Music.write_mp3(root.outdst,1.05*root.fs1,root.DATA,normalized=False)
        root.name2=root.name+'_{} ms Chorus'.format(vol.get())
        lbl.configure(text='saving "{}" finished!'.format(root.name2),font='Helvetica 10')

def importt():
    if root.filedir=='':
        root.filedir=tkinter.filedialog.askopenfilename(parent=root,title='choose music')
        root.name=str(root.filedir).split('/')
        root.name=root.name[-1].rstrip('.mp3')
    lbl.configure(text='just a sec!')
    root.update_idletasks()
    root.tmp=vol.get()
    execute()

def playy():
    if root.tmp!=vol.get():
        lbl.configure(text='just a sec!',font='Helvetica 12 bold')
        root.update_idletasks()
        execute()
    if root.ply==1:
        sd.stop()
        root.ply=0
    else:
        root.ply=1
        sd.play(root.DATA[15*root.interval:],1.05*root.fs1)

root.mainloop()