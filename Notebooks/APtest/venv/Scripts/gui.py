
def sinusoid(freq, seconds):
    nData = seconds * samplingFreq
    time = np.arange(0, nData).T/samplingFreq  # s

    # Generate a sinusoid
    amp = 1
    initPhase = np.pi/2  # rad
    sinusoid = amp*np.cos(2*np.pi*freq*time+initPhase)
    return sinusoid