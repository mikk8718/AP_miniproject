import numpy as np
from tkinter import *
import pyaudio
# from gui.py import *


root = Tk()
# root.iconbitmap('D:/HDD/Stuff/guiTest.ico')
# root.geometry("400x400") #size of the window
root.title("Mikkel is my friend")

samplingFreq = 44100 # Hz


def sinusoid(freq, seconds):
    nData = seconds * samplingFreq
    time = np.arange(0, nData).T/samplingFreq  # s

    # Generate a sinusoid
    amp = 1
    initPhase = np.pi/2 # rad
    sinusoid = amp*np.cos(2*np.pi*freq*time+initPhase)
    return sinusoid


def clickBtn(note):
    sinusoid(note, 2)

    p = pyaudio.PyAudio()

    volume = 0.5  # range [0.0, 1.0]
    duration = 2.0  # in seconds, may be float

    # generate samples, note conversion to float32 array
    samples = (np.sin(2 * np.pi * np.arange(samplingFreq * duration) * note / samplingFreq)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=samplingFreq,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    stream.write(volume * samples)

    stream.stop_stream()
    stream.close()

    p.terminate()


# myLabel1 = Label(root, text="Fuck you Mikkel")
# myLabel1.grid(row=0, column=0)


radFrame = LabelFrame(root, text="Waveforms", padx=5, pady=5)
radFrame.pack(fill=X)

sliderFrame = LabelFrame(root, text="Filters", padx=5, pady=5)
sliderFrame.pack(fill=X)

btnFrame = LabelFrame(root, text="Notes", padx=5, pady=5)
btnFrame.pack(fill=X)


btnRow = 3

n = IntVar() # only one variable to be used by multiple radiobuttons so only one of them can be active

Radiobutton(radFrame, text="Normal waveform", variable=n, value=1).pack() # grid(row=0, column=0)
Radiobutton(radFrame, text="Square waveform", variable=n, value=2).pack() # grid(row=1, column=0)
Radiobutton(radFrame, text="Triangular waveform", variable=n, value=3).pack() # grid(row=2, column=0)




btn1 = Button(btnFrame, text="A3", padx=20, pady=30, command=lambda:clickBtn(220))  # fg="white", bg="black",
# btn1.grid(row=btnRow, column=0)
btn1.pack(side=LEFT)

btn2 = Button(btnFrame, text="B3", padx=20, pady=30, command=lambda:clickBtn(246))
# btn2.grid(row=btnRow, column=1)
btn2.pack(side=LEFT)

btn3 = Button(btnFrame, text="C4", padx=20, pady=30, command=lambda:clickBtn(261))
# btn3.grid(row=btnRow, column=2)
btn3.pack(side=LEFT)

btn4 = Button(btnFrame, text="D4", padx=20, pady=30, command=lambda:clickBtn(293))
# btn4.grid(row=btnRow, column=3)
btn4.pack(side=LEFT)

btn5 = Button(btnFrame, text="E4", padx=20, pady=30, command=lambda:clickBtn(329))
# btn5.grid(row=btnRow, column=4)
btn5.pack(side=LEFT)

s1Label = Label(sliderFrame, text="Resonator").grid(row=0, column=0)
s2Label = Label(sliderFrame, text="Equalizer").grid(row=0, column=4)
placeholder = Label(sliderFrame, text="         ").grid(row=0, column=3)

slider1 = Scale(sliderFrame, from_=10, to=0)
slider1.grid(row=0, column=1)
# slider1.pack()

slider2 = Scale(sliderFrame, from_=10, to=0)
slider2.grid(row=0, column=5)
# slider2.pack()

root.mainloop()



