import abjad
from notes import notes_ann

Helmholtz_octave=[",,,",",,",",","","'","''","''","'''","''''","'''''"]
lilypod_dur=['1','2','4','8','16','32']


def make_note_sheet(music):
    violin = abjad.Violin()
    notes=[]
    for row in music:
        if row[0]=='r':
            if row[-1]:
                note=abjad.Rest(row[-2])
            else:
                note=abjad.Rest(abjad.Duration(1,int(lilypod_dur[row[-2]])))
        else:
            x=notes_ann[row[0]].lower()
            if x[-1]=='#' or x[-1]=='b':
                x=x[0]
                x=x+'s'
            note_=x
            oct_=Helmholtz_octave[row[1]]
            due_=lilypod_dur[row[-2]]
            note=abjad.Note(note_+oct_+due_)
        notes.append(note)  
    abjad.attach(violin, notes[0])
    container = abjad.Container(notes)
    abjad.show(container)        
    return


        

 
