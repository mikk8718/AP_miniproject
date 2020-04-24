import numpy as np

samplingFreq = 44100 # Hz


def sinusoid(freq, seconds):
    nData = seconds * samplingFreq
    time = np.arange(0, nData).T/samplingFreq # s

    # Generate a sinusoid
    amp = 1;
    initPhase = np.pi/2 # rad
    sinusoid = amp*np.cos(2*np.pi*freq*time+initPhase)
    return sinusoid

def sound(note):
    if note == "C":
        return sinusoid(261.63, 0.2)
    if note == "D":
        return sinusoid(293.66, 0.2)
    if note == "E":
        return sinusoid(329.63, 0.2)
    if note == "-":
        return sinusoid(0, 0.2) * 0
    if note == " ":
        return sinusoid(0, 0.5) * 0