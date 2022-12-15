---
title: Maths Behind Vibration Analysis
permalink: /maths/
layout: single
---
In our project, we explored two different ways of analyzing vibrations: one using the fast fourier transform (FFT) to get the data in the frequency domain, another using the power spectral density (PSD) to normalize the DFT data to reduce the amount of random vibrations.

## Fast Fourier Transform (FFT)
For our MVP analysis, we will be taking fast fourier transforms (FFTs) of fragments of the data collected by the accelerometer to convert the data to the frequency domain. Since we are analyzing the data set of a car whose engine revolutions are not necessarily constant, we will take scrolling data of 5 seconds' worth of data. A second's worth of data that was sampled at 200Hz will be 200 points. Although it's not a power of 2, it is still a sufficient amount of data find the revolutions per minute (RPM) of an engine running at less than 5500 RPM, which is more than sufficient for our purposes.

To prove this to ourselves, the Nyquist Frequency is twice the frequency we are trying to measure. Assuming a maximum RPM of 5500, we would need to sample at a rate just above 11000 RPM, or 183.33 Hz. Since 200Hz is greater than 183.33Hz, we can assume that we are okay. It is valuable, however, that MATLAB Mobile technically said that we were sampling at 100 Hz, which would reduce our accuracy down to just shy of 3000 RPM. However, when looking at the sampled data, we actually found that the data was recorded in 200Hz, giving us the 200 points per second.

To analyze the frequencies as the car accelerates and decelerates, we will take the FFT of the one-second window. We will do this for every second we partition. To recap, the FFT algorithm helps us compute the discrete Fourier transform (DFT). Since we are computing the DFT of a 1000 point sample, we will get a 1000 by 1000 DFT matrix.

![DFT Matrix](/media/images/FFTmatrix.PNG)
_Figure 1: FFT matrix that gets multiplied to our data to convert from the time domain to the frequency domain. N is the number of points in the data set._

Where the W (weight) is calculated by the following equation

![W calculation](/media/images/FFTW^n.PNG)

_Figure 2: Weight equation for the nth index of a FFT of N points. j is the square root of -1._

This all gets multiplied to the original data set x, to produce the data in the frequency domain represented by the following equation.

![Data in Frequency Domanin](/media/images/newDFT.PNG)

_Figure 3: Data X(k) in terms of the frequency domain for N points where the data matrix x(n) is multiplied by the weights._

By scrolling through FFTs, we can stitch them together to create a short film that displays how frequency intensities evolve as the car drives. Watching a replay of the FFT film allows us to see the the RPM grow as we accelerate the vehicle. We can also see other frequencies develop and appear as the car drives. 

Unfortunately, the frequencies recorded by the accelerometer also contain a lot of external frequencies that are not necessarily related to the vehicle, such as road imperfections or changes in elevation. In order to better understand the frequencies produced by the vehicle, we must be able to normalize the data such that road imperfections or other random vibrations are reduced from the data set, and the frequencies that appear the most will show up with greater amplitude. To do this, we must calculate a power spectrum density (PSD).

## Power Spectral Densiy (PSD)
A PSD takes the FFT matrix (which is a matrix of complex numbers) and multiplies it with its complex conjugate. It then divides this by the frequency step. We must also divide by 2 to convert the amplitude to be rms^2/Hz (rms being root mean squared). Note, the PSD is the limit of these operations as the frequency step approaches 0. Below is a representation of this equation.

![PSD Equation](/media/images/psd.PNG)

_Figure 4: Equation to calculate the PSD, where Δf is the frequency step (1/time) and X*(f) is the complex conjugate of the FFT X(f)._

In this data, we will be able to see the intensity of different frequencies as we drive them. Thus, instead of having to chunk down smaller windows like the scrolling FFT, we can simply take the PSD of the entire data set once. 