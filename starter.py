import tkinter as tk
import subprocess, threading
import tkinter.messagebox
import sounddevice as sd
import tkinter.filedialog as tkf



class ThreadedCall(threading.Thread):

	def __init__(self, command):
		self.command = command
		threading.Thread.__init__(self)
	 
	def run(self):
		process = subprocess.Popen(self.command)

class Launcher(tk.Frame):
	"""Launcher/menu screen for project components."""
	
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Launcher")
		tk.Frame.__init__(self, self.root)
		self.buttonOptions = {'fill': 'both', 'padx': 10, 'pady': 10 }
		self.drawText()
		self.drawButtons()
		
	def Choruss(self):
        
		Chorusapp = ThreadedCall(["python", "Chorus.py"])
		Chorusapp.start()
        
        
	def launchTranscription(self):
        
		transcribeapp = ThreadedCall(["python", "Audio_Sheet.py"])
		transcribeapp.start()

        
	def deffect(self):
        
		deffectapp = ThreadedCall(["python", "3Deffect.py"])
		deffectapp.start()

	def drawButtons(self):
		buttons = [tk.Button(self, text="3D effect & Bass boosting",command=self.deffect)]
		buttons += [tk.Button(self, text="Audio-Sheet Transcription", command=self.launchTranscription)]
		buttons += [tk.Button(self, text="Chorus",command=self.Choruss)]
		buttons += [tk.Button(self, text="Quit", command=lambda:self.root.destroy())]
		for button in buttons:
			button.pack(**self.buttonOptions)
			
	def drawText(self): 
		lbl=tk.Label(self, text="Choose an app to launch and Wait!").pack(side='top')
		
	
	def run(self):
		self.pack()
		self.root.mainloop()
		
if __name__ == '__main__':	
	launcher = Launcher()
	launcher.run()