import numpy as np
from math import log2

notes= ['A', 'A#', 'B', 'C', 'C#', 'D', 'Eb', 'E'
            , 'F', 'F#', 'G']
   
Matrix = [[0 for x in range(7)] for y in range(11)] 
for i in range(11):
    for j in range(3,7):
        Matrix[i][j]=round((27.5*2**j)*2**(i/12),ndigits=2)


class noteprocessing:
    @staticmethod         
    def getFrequency(p,f):
        arr,MAX1,frequency1,=[],0,0
        for i in range(0,300):
            arr.append([p[i],np.abs(f[i])])
        arr.sort(key=lambda x:x[1])
        [frequency1,MAX1]=arr[-1] #maximum
        return round(frequency1,ndigits=1),MAX1


    @staticmethod
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx
    
    @staticmethod
    def getNote(frequency):
        idx=noteprocessing.find_nearest(Matrix,frequency)
        octave=idx%7
        note_id=notes[int(idx/7)]
        return octave,note_id
                

    @staticmethod
    def getBit_id(rawnotes):
        notelist=[]
        for i in range(len(rawnotes)):            
            repeat=1
#            sum_domain=rawnotes[i][2]*rawnotes[i][1]
            while(True):
                try:
                    if rawnotes[i]==rawnotes[i+1]:
#                        sum_domain=sum_domain+rawnotes[i+1][2]*rawnotes[i+1][1]
                        repeat=repeat+1
                        i+=1
                    else:
                        break
                except:
                    break
            try:
                if notelist[-1][0]!=rawnotes[i]:
                    notelist.append([rawnotes[i],repeat])
            except: #error occured for the firs append
                    notelist.append([rawnotes[i],repeat])
        return notelist
    
    
    

            


            
    