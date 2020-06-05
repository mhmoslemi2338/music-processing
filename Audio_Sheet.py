import tkinter as tk
import tkinter.filedialog
import subprocess, threading
from tkinter import ttk
from Music import *
from notes import *
from ppp import *
import save_to_pdf
from scipy.signal import butter, lfilter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

T=0.05
rawnotes=[]#each note is 50ms
freqq=[]
domainn=[]


def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def progressbarr(i,data1):
    prog=round(100*(i/len(data1)))
    if prog==100:
        prog=0
        lbl2=lbl.configure(text= '   Ready !   ',font='Helvetica 12 bold')
    else:
        lbl2=lbl.configure(text= '\tprogress:\t' + str(prog)+'%\t',font='Helvetica 12 bold')
    progress_var.set(prog)
    top.update_idletasks()
    return

def execute(lowfreq,hifreq):
    fs1,data1=Music.read_mp3(top.filedir)  
    top.data1=data1
    top.fs1=fs1
    interval=int(fs1*T)
    top.interval=interval
    
    for i in range(0,len(data1),interval):
        DATA=butter_bandpass_filter(data1[i:i+interval,0], lowfreq, hifreq, fs1)
        f,p=Music.frequencies(DATA,fs1)  
        freq,domain=noteprocessing.getFrequency(p,f)
        freqq.append(freq)
        domainn.append(domain)
        progressbarr(i,data1)
   
    for i in range(len(freqq)):
        if domainn[i]>400000:
            octave,note_id=noteprocessing.getNote(freqq[i])
            rawnotes.append(note_id+str(octave))   
            
    notelist=noteprocessing.getBit_id(rawnotes)
    music,music_sheet=Music.get_music_array(notelist)
    return music,music_sheet,fs1

  

  


########################## --- GUI --- ######################################
    
top=tk.Tk()
#variables
top.title('Audio-Sheet')
top.interval,top.fs1,top.ply=0,0,0
top.music_sheet,top.y,top.data1,top.music=[],[],[],[]
top.filedir,top.outdst='',''
#labels
lbl=tk.Label(top, text="\tprogress: 0%\t",font='Helvetica 12 bold')
lbl.grid(row=1,column=0)
tk.Label(top,text='cutoff (low) frequency(Hz):',font='Helvetica 12').grid(row=2,pady=2,column=0)
tk.Label(top,text='cutoff (high) frequency(Hz):',font='Helvetica 12' ).grid(row=3,pady=2,column=0)
#progress bar
progress_var=tk.DoubleVar()
progress = ttk.Progressbar(top,variable=progress_var, orient = 'horizontal', length = 250, mode = 'determinate')
progress=progress.grid(row=1,column=1,pady=5)
#entries
e1 = tk.Entry(top)
e2 = tk.Entry(top)
e1.grid(row=2, column=1)
e2.grid(row=3, column=1)
e1.insert(10,'220')
e2.insert(10,'1200')
#figures
figure = Figure(figsize=(4, 3.6), dpi=100)
canvas = FigureCanvasTkAgg(figure, top)
canvas.get_tk_widget().grid(row=0, column=0)
figure = Figure(figsize=(4, 3.6), dpi=100)
canvas = FigureCanvasTkAgg(figure, top)
canvas.get_tk_widget().grid(row=0, column=1)
#buttons
tk.Button(top, text="\tget note sheet\t",command=lambda:showpdf()).grid(pady=5,row=5,column=1)
tk.Button(top, text="\timport mp3 file\t",command=lambda:importfile()).grid(pady=5,row=4,column=1)
tk.Button(top, text="\tsave output mp3\t",command=lambda:save_mp3()).grid(pady=5,row=6,column=1)
tk.Button(top, text="\tplay/stop\t",command=lambda:playy()).grid(padx=0,pady=5,row=4,column=0)
tk.Button(top, text="\tplot\t",command=lambda:pausee()).grid(pady=5,row=5,column=0)
tk.Button(top, text="\tBack\t", command=lambda:top.destroy()).grid(pady=5,row=6,column=0)

#functions
def pausee():
    oo=len(top.data1)
    oo=int(oo*0.3)
    E1=int(e1.get())
    E2=int(e2.get())
    DATA=butter_bandpass_filter(top.data1[oo:oo+top.interval,0], E1, E2, top.fs1)
    
    figure = Figure(figsize=(4, 3.6), dpi=100)
    plot = figure.add_subplot(1,1 , 1)
    plot.plot(DATA,linewidth=0.8)
    # figure.title('fff')
    plot.set_title('filtered signal with {} Hz-{} Hz BP-filter'.format(E1,E2))
    ww=round(oo/top.interval *0.05,ndigits=2)
    plot.set_xticklabels([0,ww,round(ww+0.01,ndigits=2),round(ww+0.02,ndigits=2),round(ww+0.03,ndigits=2),round(ww+0.04,ndigits=2)])
    plot.set_xlabel('time(sec)')
    plot.set_yticklabels([])
    canvas = FigureCanvasTkAgg(figure, top)
    canvas.get_tk_widget().grid(row=0, column=1)
      
def importfile():
    E1=e1.get()
    E2=e2.get()
    if E1=='' or E2=='':
        tk.messagebox.showwarning( message='fill the Blanks')
    else:
        try:
            E1=int(E1)
            E2=int(E2)
            if E2<=E1:
                tk.messagebox.showwarning(message='high frequency must be bigger than low frequency')             
            else:
               top.filedir=tkinter.filedialog.askopenfilename(parent=top,title='choose music')
               [top.music,top.music_sheet,top.fs1]=execute(E1,E2)
               oo=len(top.data1)
               oo=int(oo*0.3)
               figure = Figure(figsize=(4, 3.6), dpi=100)
               plot= figure.add_subplot(1,1 , 1)
               plot.plot(top.data1[oo:oo+top.interval,0],linewidth=0.8)
               plot.set_title('noisy signal in arbitrary 50ms interval')
               ww=round(oo/top.interval *0.05,ndigits=2)
               plot.set_xticklabels([0,ww,round(ww+0.01,ndigits=2),round(ww+0.02,ndigits=2),round(ww+0.03,ndigits=2),round(ww+0.04,ndigits=2)])
               plot.set_yticklabels([])
               plot.set_xlabel('time(sec)')
               canvas = FigureCanvasTkAgg(figure, top)
               canvas.get_tk_widget().grid(row=0, column=0)
        except:
            tk.messagebox.showwarning( message='fill the Blanks with integers') 
  
def showpdf():
    if top.music_sheet==[]:
        tk.messagebox.showwarning( message='first import mp3 file!')
    else:
        lbl2=lbl.configure(text= ' \t  just a sec ! \t ',font='Helvetica 12 bold')
        top.update_idletasks()
        save_to_pdf.make_note_sheet(top.music_sheet) 
        lbl2=lbl.configure(text= '   Ready !   ',font='Helvetica 12 bold')
 
def save_mp3():   
    if top.music==[]:
        tk.messagebox.showwarning( message='first import mp3 file!')
    else:
        top.outdst=tkinter.filedialog.askdirectory(parent=top,title='choose music')
        y = get_music(top.music, top.fs1)
        top.y=y
        top.outdst=str(top.outdst)+'/out.mp3'
        Music.write_mp3(top.outdst,top.fs1,y,normalized=True)
        lbl2=lbl.configure(text= '   Done !   ',font='Helvetica 12 bold')
        tk.messagebox.showwarning( message='Done !')
        lbl2=lbl.configure(text= '   Ready !   ',font='Helvetica 12 bold')
        
def playy():
    if top.ply==1:
        sd.stop()
        top.ply=0
    else:
        top.y = get_music(top.music, top.fs1)
        top.ply=1
        sd.play(top.y)
        

top.mainloop()

