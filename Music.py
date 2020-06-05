import pydub
import numpy as np
from notes import notes_ann
from notes import notes_duration
from abjad import Duration


class Music:
    @staticmethod
    def read_mp3(filename, normalized=False):
        a = pydub.AudioSegment.from_mp3(filename)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, 2))
        if normalized:
            return a.frame_rate, np.float32(y) / 2**15
        else:
            return a.frame_rate, y
    
    @staticmethod
    def write_mp3(filename, Fs, x, normalized=False):
        channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
        if normalized:  
            y = np.int16(x * 2 ** 15)
        else:
            y = np.int16(x)
        song = pydub.AudioSegment(y.tobytes(), frame_rate=Fs, sample_width=2, channels=channels)
        song.export(filename, format="mp3", bitrate="320k")
        return  
    
    @staticmethod
    def frequencies(x, fs):
        Fd = np.fft.fft(x)
        Fx = np.linspace(0, 1, max(x.shape))*fs
        return Fd, Fx

    
    @staticmethod
    def get_music_array(notelist):
        music_play,music_sheet=[],[]
        for row in notelist:
            if row[1]>1:    
                if row[0]!='r':
                    tmp=row[0][0:2]
                    if tmp[1]!='#' and tmp[1]!='b':
                        tmp=tmp[0]
                    dur0=row[1]
                    if dur0 in [2,3,4]:
                        dur=5 #Demisemiquaver
                    elif dur0 in [5,6,7]:
                        dur=4 #Semiquaver 
                    elif dur0 in [8,9,10]:
                        dur=3 #Quaver
                    elif dur0 in [11,12,13]:
                        dur=2 #Crotchet 
                    elif dur0 in [14,15,16]:
                        dur=1 #Minim
                    else:
                        dur=0 #Semibreve
                    music_play.append([notes_ann.index(tmp),int(row[0][-1]),dur])
                    music_sheet.append([notes_ann.index(tmp),int(row[0][-1]),dur,0])
                else:
                    dur0=row[1]
                    if dur0<20:
                        dur=6-round(dur0/3)
                        if dur<3:
                            music_sheet.append(['r','',dur,0])
                    else:
                        dur=round(row[1]/18)
                        if dur>4:
                            dur=4
                        dur=Duration(dur,1)
                        music_sheet.append(['r','',dur,1])           
        return music_play,music_sheet
    
    