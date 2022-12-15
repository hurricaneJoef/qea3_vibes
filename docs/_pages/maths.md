---
title: Maths Behind Vibration Analysis
permalink: /maths/
layout: single
---

For our main analysis, we will be taking fast fourier transforms (FFTs) of fragments of the data collected by the accelerometer. Since we are analyzing the data set of a car whose engine revolutions are not necessarily constant, we will take scrolling data of a second's worth of data. A second's worth of data that was sampled at 200Hz will be 200 points. Although it's not a power of 2, it is still a sufficient amount of data find the revolutions per minute (RPM) of an engine running at less than 5500 RPM, which is more than sufficient for our purposes.

To prove this to ourselves, the Nyquist Frequency is twice the frequency we are trying to measure. Assuming a maximum RPM of 5500, we would need to sample at a rate just above 11000 RPM, or 183.33 Hz. Since 200Hz is greater than 183.33Hz, we can assume that we are okay. It is valuable, however, that MATLAB Mobile technically said that we were sampling at 100 Hz, which would reduce our accuracy down to just shy of 3000 RPM. However, when looking at the sampled data, we actually found that the data was recorded in 200Hz, giving us the 200 points per second.

To analyze the frequencies as the car accelerates and decelerates

By scrolling through FFTs, we can stitch them together to create a short film that displays how frequency intensities evolve as the car drives. We can detect the rpm by tracking the peaks and generating 