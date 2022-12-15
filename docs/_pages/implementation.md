---
title: Our Product
permalink: /implementation/
layout: single
---

_TODO: Briefly discuss how the code works and what it gives us_
Our code uses audio collected with the vibrations as a duration indicator for the length of our film. We also include the audio as a means of synchronizing what we see with the acceleration of the vehicle (at the least, audibly). Then we calculated the sampling frequency by assuming that all of the points are equidistant from each other. In doing so, we got a sampling frequency of about 200hz. 

We then took the acceleration data from the accelerometer data was then converted to a magnitude. We then took the average of the entire data data subtracted it from the original data. It was then plugged into `matpltlib.plt.psd` to generate the power spectrum density (PSD) plot that we later analyzed.

The rolling frame FFT (fast fourier transform) where every frame samples the 5 seconds before it and takes an fft of that data except at the start of the video. the reason we chose python is becuase we could easlily create an animation of the = "rolling" fft (and becuase we didnt want to deal with matlab's 1 based indexing)