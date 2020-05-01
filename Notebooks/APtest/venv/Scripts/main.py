import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import pyaudio
import scipy
from scipy import signal
from scipy.fftpack import rfft, irfft, fftfreq


root = Tk()
# root.iconbitmap('D:/HDD/Stuff/guiTest.ico')
# root.geometry("400x400") #size of the window
root.title("Mikkel is my friend")

samplingFreq = 44100  # Hz


def waveform(data, freq: int, time, input_) -> list:
    t = np.linspace(0, 5, 44100)
    output = np.copy(data)
    output_triangle = np.zeros(np.size(data))
    print(data)
    print((-(1/2)*np.sin(2 * np.pi * 2 * freq * time)))

    if input_ == 2:     # SQUARE WAVE
        # squareWave = np.sign(np.sin(2*np.pi*sinusoid/freq/nData))
        # for index, value in enumerate(data):
        #     if value >= 0:
        #         output[index] = 1
        #     else:
        #         output[index] = -1
        # return output
        return scipy.signal.square(data, 0.5)

    elif input_ == 3:  # TRIANGULAR WAVE

        print("sawtooth", scipy.signal.sawtooth(2 * np.pi * freq * t, 0.5))
        return scipy.signal.sawtooth(data, 0.5)

        # return data
    elif input_ == 1:  # NORMAL WAVE
        return data


def clickBtn(note):
    # sinusoid(note, 1)

    p = pyaudio.PyAudio()

    volume = 0.1  # range [0.0, 1.0]
    duration = 1.0  # in seconds, may be float

    # generate samples, note conversion to float32 array
    samples = (np.sin(2 * np.pi * np.arange(samplingFreq * duration) * note / samplingFreq)).astype(np.float32)
    # samples = np.sin(np.pi/2)
    samples2 = waveform(samples, note, 1, n.get())
    # for paFloat32 sample values must be in range [-1.0, 1.0]

    filtered = highpass(samples2, slider3.get())
    filtered2 = lowpass(filtered, slider2.get())
    filtered3 = ResonatorFilter(samples2, 440, 100, 50)

    # plt.plot(filtered3)
    # plt.xlim(0, 1000)
    # plt.show()


    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=samplingFreq,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    stream.write(volume * filtered2)

    stream.stop_stream()
    stream.close()

    p.terminate()


def highpass(input_, cutoff):
    # time = np.arange(0, samplingFreq).T/samplingFreq  # s
    nData = 1 * 44100
    time = np.arange(0, nData).T / 44100
    W = fftfreq(nData, d=time[1]-time[0])
    f_signal = rfft(input_)
    # If our original signal time was in seconds, this is now in Hz
    cut_f_signal = f_signal.copy()
    cut_f_signal[(W/2 > cutoff)] = 0

    cut_signal = irfft(cut_f_signal)
    return cut_signal


def lowpass(input_, cutoff):
    # time = np.arange(0, samplingFreq).T/samplingFreq  # s
    nData = 1 * 44100
    time = np.arange(0, nData).T / 44100
    W = fftfreq(nData, d=time[1]-time[0])
    f_signal = rfft(input_)
    # If our original signal time was in seconds, this is now in Hz
    cut_f_signal = f_signal.copy()
    cut_f_signal[(W/2 < cutoff)] = 0

    cut_signal = irfft(cut_f_signal)
    return cut_signal


def ResonatorFilter(inputSignal,samplingFreq,centerFregValue,BandwidthValue):
    centerFreq = 2*np.pi*centerFregValue/samplingFreq
    bandwidth = 2*np.pi*BandwidthValue/samplingFreq

    poleRadius = (2 - bandwidth) / 2
    poleAngle = np.arccos(2 * poleRadius * np.cos(centerFreq) / (1 + poleRadius ** 2))
    gain = (1 - poleRadius ** 2) * np.sin(poleAngle)
    outputSignal = np.array([gain*inputSignal + 2 * poleRadius * np.cos(poleAngle), -poleRadius ** 2])
    return outputSignal


# btnRow = 3

############################ GUI ####################################

radFrame = LabelFrame(root, text="Waveforms", padx=5, pady=5)
radFrame.pack(fill=X)

sliderFrame = LabelFrame(root, text="Filters", padx=5, pady=5)
sliderFrame.pack(fill=X)

btnFrame = LabelFrame(root, text="Notes", padx=5, pady=5)
btnFrame.pack(fill=X)

n = IntVar() # only one variable to be used by multiple radiobuttons so only one of them can be active
n.set("1")

Radiobutton(radFrame, text="Normal waveform", variable=n, value=1).pack(anchor="w")  # grid(row=0, column=0)
Radiobutton(radFrame, text="Square waveform", variable=n, value=2).pack(anchor="w")  # grid(row=1, column=0)
Radiobutton(radFrame, text="Triangular waveform", variable=n, value=3).pack(anchor="w")  # grid(row=2, column=0)


btn1 = Button(btnFrame, text="A3", padx=20, pady=30, command=lambda:clickBtn(220))  # fg="white", bg="black",
# btn1.gri, anchor="w"d(row=btnRow, column=0)
btn1.pack(side=LEFT)

btn2 = Button(btnFrame, text="B3", padx=20, pady=30, command=lambda:clickBtn(246))
# btn2.grid(row=btnRow, column=1)
btn2.pack(side=LEFT)

btn3 = Button(btnFrame, text="C4", padx=20, pady=30, command=lambda:clickBtn(261))
# # btn3.grid(row=btnRow, column=2)
btn3.pack(side=LEFT)
#
btn4 = Button(btnFrame, text="D4", padx=20, pady=30, command=lambda:clickBtn(293))
# # btn4.grid(row=btnRow, column=3)
btn4.pack(side=LEFT)
#
btn5 = Button(btnFrame, text="E4", padx=20, pady=30, command=lambda:clickBtn(329))
# # btn5.grid(row=btnRow, column=4)
btn5.pack(side=LEFT)

s1Label = Label(sliderFrame, text="Resonator").grid(row=0, column=0)
s2Label = Label(sliderFrame, text="Equalizer").grid(row=0, column=4)
placeholder = Label(sliderFrame, text="         ").grid(row=0, column=3)


slider1 = Scale(sliderFrame, from_=5000, to=0)
slider1.grid(row=0, column=1)
# slider1.pack()

slider2 = Scale(sliderFrame, from_=1000, to=0)
slider2.grid(row=0, column=5)
# slider2.pack()

slider3 = Scale(sliderFrame, from_=1000, to=0)
slider3.grid(row=0, column=6)


root.mainloop()



