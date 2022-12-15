---
title: Our Product
permalink: /implementation/
layout: single
---

The language of choice for our implementation is Python. One of the reasons for our use of python is our personal familiarity with the language. More importantly, we felt that generating the film would be easier in Python by using the MoviePy library.

Our code uses audio collected with the vibrations as a duration indicator for the length of our film. We also include the audio as a means of synchronizing what we see with the acceleration of the vehicle (at the least, audibly). Then we calculated the sampling frequency by assuming that all of the points are equidistant from each other. In doing so, we got a sampling frequency of about 200hz. 

We then took the acceleration data from the accelerometer data was then converted to a magnitude. We then took the average of the entire data data subtracted it from the original data. It was then plugged into `matpltlib.plt.psd` to generate the power spectrum density (PSD) plot that we later analyzed.

The rolling frame FFT (fast fourier transform) is created by chunking the data into 5 second windows. We do this by starting at a point, and simply taking the data of 5 seconds later. For this reason, our data does not begin to update until after the 5 second start. Then, the point immediately after the the starting point becomes the new starting point to do the same thing again. We then simply plug in the data indexed at these times and take its FFT. We used numpy's fft functon to do this.