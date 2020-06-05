from starter import tk,sd,tkf
from Music import *
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
import math


T=0.05
rawnotes=[]#each note is 50ms
freqq=[]
domainn=[]
r=1
l=1
inp=0
#160=8sec/0.05sec
move=np.linspace(-0.95,0.95,160)


def execute():    
    fs1,data1=Music.read_mp3(root.filedir) 
    root.sample = AudioSegment.from_mp3(root.filedir)
    interval=int(fs1*T)
    DATA=data1
    
    if root.varr2.get()==1:
        for i in range(0,len(data1),interval):
            if int(int(i/interval)/len(move))%2==0:
                inp=move[int(i/interval)%len(move)]
            else:
                inp=move[-(1+int(i/interval)%len(move))]
            DATA[i:i+interval,0]=np.multiply(data1[i:i+interval,0],0.7*(l-inp))
            DATA[i:i+interval,1]=np.multiply(data1[i:i+interval,1],0.7*(r+inp))
            lbl.configure(text='side-side is 8 sec',font='Helvetica 11')
            root.update_idletasks()
    else:
        for i in range(0,len(data1),interval):
            inp=root.scale_var.get()
            DATA[i:i+interval,0]=np.multiply(data1[i:i+interval,0],0.7*(l-inp))
            DATA[i:i+interval,1]=np.multiply(data1[i:i+interval,1],0.7*(r+inp))
        lbl.configure(text='ready to play!',font='Helvetica 12 bold')
        root.update_idletasks()
    root.DATA=DATA
    root.fs1=fs1
    



def bass_line_freq(track):
    sample_track = list(track)
    est_mean = np.mean(sample_track)
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))
    bass_factor = int(round((est_std - est_mean) * 0.005))
    return bass_factor
attenuate_db = 0
accentuate_db = 1.8




########################## --- GUI --- ######################################


root=tk.Tk()
#variables
root.title('3Deffect & Bass boosting')
root.play,root.tmp,root.fs1,root.ply,root.interval=0,0,0,0,0
root.outdst,root.filedir,root.name,root.name2='','','',''
root.DATA=[]
root.varr2 = tk.IntVar()
scale_var = tk.DoubleVar()
scale_var2 = tk.DoubleVar()
scale_var.set(0)
scale_var2.set(0)
root.varr2.set(1)
root.scale_var=scale_var


#labels
lbl=tk.Label(root, text="",font='Helvetica 12 bold')
lbl.grid(row=1,column=0,pady=5,padx=5)
tk.Label(root,text='\n\tLeft - Right :',font='Helvetica 12').grid(row=1,padx=4,pady=10,column=1)
tk.Label(root,text='\tUp - Down :',font='Helvetica 12').grid(row=0,padx=4,pady=10,column=1)
#buttons
tk.Button(root, text="import",font='bold',width=15,command=lambda:importt()).grid(pady=10,padx=20,row=2,column=0)
tk.Button(root, text="play/stop",font='bold',width=15,command=lambda:playy()).grid(padx=10,pady=20,row=2,column=1)
tk.Button(root, text="save",font='bold',width=15,command=lambda:savee()).grid(padx=1,pady=10,row=7,column=1)
tk.Button(root, text="Back",font='bold', command=lambda:root.destroy(),width=15).grid(pady=5,padx=1,row=7,column=0)
tk.Button(root, text="apply",font='bold', command=lambda:aplyy(),width=15).grid(pady=5,padx=1,row=2,column=2)
tk.Button(root, text="save Bass boosted",font='bold', command=lambda:bassb(),width=15).grid(pady=5,padx=1,row=7,column=2)
#volume bars
vol1 = tk.Scale(root,from_ = -1,to = 1,orient = tk.VERTICAL ,resolution = 0.1,variable=scale_var2,length=150)
vol = tk.Scale(root,from_ = -1,to = 1,orient = tk.HORIZONTAL ,resolution = 0.1,variable=scale_var,length=150)
vol.grid(row=1,pady=0,padx=20,column=2)
vol1.grid(row=0,pady=0,padx=20,column=2)
#check box
chb=tk.Checkbutton(root, text="Auto",variable=root.varr2)
chb.grid(row=0,pady=50,padx=20,column=0)



#functions
def bassb():
    if root.filedir!='':
        root.outdst=tkf.askdirectory(parent=root,title='choose music')
        root.outdst=root.outdst+'/'+root.name + "_Bass-boosted.mp3"
        
        lbl.configure(text=' just a sec!',font='Helvetica 12 bold')
        root.update_idletasks()
        filtered = root.sample.low_pass_filter(bass_line_freq(root.sample.get_array_of_samples()))
        combined = (root.sample - attenuate_db).overlay(filtered + accentuate_db)
        combined.export(root.outdst, format="mp3")
        lbl.configure(text='saving finished!',font='Helvetica 12')

def savee():
    if root.filedir!='':
        if root.tmp!=vol.get():
            lbl.configure(text=' just a sec!',font='Helvetica 12 bold')
            root.update_idletasks()
            execute()
        root.outdst=tkf.askdirectory(parent=root,title='choose music')
        root.outdst=str(root.outdst)+'/'+root.name+'_3D.mp3'
        Music.write_mp3(root.outdst,root.fs1,root.DATA,normalized=False)
        lbl.configure(text='saving finished!',font='Helvetica 12')

def importt():
    # if root.filedir=='':
    root.filedir=tkf.askopenfilename(parent=root,title='choose music')
    root.name=str(root.filedir).split('/')
    root.name=root.name[-1].rstrip('.mp3')
    lbl.configure(text=' just a sec!')
    root.update_idletasks()
    root.tmp=vol.get()
    execute()

def aplyy():
    lbl.configure(text=' just a sec!',font='Helvetica 12 bold')
    root.update_idletasks()
    root.tmp=vol.get()
    execute()
 
def playy():
    if root.ply==1:
        sd.stop()
        root.ply=0
    else:
        root.ply=1
        sd.play(root.DATA,)
    
root.mainloop()