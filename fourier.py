#!/bin/python2
import numpy as np
import matplotlib.pyplot as plt

#signal = [1,2,3,2,4,2,7,2,30,4]*2
signal = np.random.random_sample(6)

fourier = np.fft.fft(signal)
freq = np.fft.fftfreq(len(signal))

print fourier, freq


x = np.arange(0, len(signal), 0.01);
ye = [0] * len(x)

for i, c in enumerate(fourier):
    amp = np.abs(c)/len(signal)
    pha = np.arctan2(np.imag(c), np.real(c))
    #print amp, pha
    if amp != 0:
        #y = amp*np.cos((x + pha)*2*np.pi/freq[i])
        y = np.real(c)*np.cos(2*np.pi*x*freq[i]) - np.imag(c)*np.sin(2*np.pi*x*freq[i])
        y = y/len(signal)
        #y = np.cos(x*freq[i])
        #y = np.real(c*np.exp(1j*2*np.pi*x*freq[i]))/len(signal)
        plt.plot(x, y, ':')
        ye = np.add(ye, y)

plt.plot(x, ye)

plt.plot(range(len(signal)),signal, 'o')

plt.show()
