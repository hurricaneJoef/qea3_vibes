---
title: Our Results
permalink: /results/
layout: single
---

One of the outputs of running `main.py` is an mp4 file containing the rolling FFTs movie. The following is an example of 3 and a half minutes worth of driving around. 

 [![FFT video](https://img.youtube.com/vi/avx26oCtKyk/0.jpg)](https://www.youtube.com/watch?v=avx26oCtKyk) 

_Video: FFT film produced by `main.py`_
In the video, there are moments where we are able to see a few interesting spikes. Knowing how we drove the vehicle around the times the spikes showed up gave us a few insights.

## FFT Video Frames

### Idle
![Idle Spectra](/media/images/Idle.png)

_Figure 1: FFT while idling at the end of a drive_

At idle, this is what the spectra looks like - appearing that the idle RPM is around 2000, instead of 500-600 (which is the typical idle RPM for the vehicle). Noting that the engine is a 4 cycle V6, this data begins to make sense. It would appear that the frequency we are detecting is from the exhaust, since we are getting 4 times the RPM that we are expecting. This is good in the sense that we are collecting data, but poor because we would need 4 times the sampling rate to account for 4 times the RPM. With the current window, our trackable RPMs go down to 1375. This is bad in terms of tracking *our* data; however, it doesn't mean that we can't get any data. This is good news because it means that the driveshaft is not broken or otherwise damaged since we are not detecting those vibrations.

### Left Turn
![Turning_Left](/media/images/Turning_Left.png)

_Figure 2: FFT while taking a left turn_

We notiched this spike arise while we were taking a left turn. Notably, this spike did not occur in this fashion until we took another left turn. If it was just for the spetra alone, we would not have been able to determine that this was likely the right wheel bearings. This is because this issue is speed dependent. In theory we could find the speed if we had the gear, RPM, and differential ratios, but none of those are apparent in this spectra.

### Possibly 1125 RPM?
![Possibly 1125 RPM](/media/images/Interesting.png)

_Figure 3: FFT of an interesting isolated spike_

This spike was interesting to us at first since it was very isolated, and no noise was really apparent. Once considering the first issue, we can deduce that this could very well be an instance where we got clean spectra of our RPM, this is notable since the car was slowing down at this specific instance

## PSD outputs
![Full PSD](/media/images/sensorlog_20221212_144004.csv.png)
![Gear PSD](/media/images/sensorlog_20221212_144004.csvgears.png)

