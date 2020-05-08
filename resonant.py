import scipy.io.wavfile as wave
import numpy as np
import sounddevice as sd

sampleFreq, signal = wave.read("guitar.wav")

def resonance(inputsignal, sampleFreq, a, b):
    #centerFrequency = 2*np.pi*((sampleFreq/100)*a)/sampleFreq # make the centerFreq scalable by 0-100% of the samplingFreq
    #bandwidth = 2*np.pi*((sampleFreq/100)*b)/sampleFreq # make the bandwidth scalable by 0-100% of the samplingFreq


    centerFrequency = 2 * np.pi * a / sampleFreq
    bandwidth = 2 * np.pi * b / sampleFreq

    poleRadius = (2 - bandwidth) / 2
    poleAngle = np.arccos(2 * poleRadius * np.cos(centerFrequency) / (1 + poleRadius**2))
    gain = (1 - poleRadius**2) * np.sin(poleAngle)

    length = np.size(inputsignal)
    output = np.zeros(length)
    iirCoefficients = np.array([2*poleRadius*np.cos(poleAngle), -poleRadius**2])
    print(iirCoefficients[0])
    print(iirCoefficients[1])

    for n in np.arange(length):
        if n < 2:
            output[n] = inputsignal[n]
        else:
            output[n] = gain * inputsignal[n] + 2 * poleRadius * np.cos(poleAngle) * output[n - 1] - poleRadius**2 * output[n - 2]
            #output[n] = inputsignal[n] + iirCoefficients[0] * output[n - 1] - iirCoefficients[1] * output[n - 2]
    return output / max(output)

sd.play(resonance(signal, sampleFreq, 1000, 500), sampleFreq)
#sd.play(signal, sampleFreq)
sd.wait()

