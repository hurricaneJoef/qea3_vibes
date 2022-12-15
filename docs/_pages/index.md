---
title: Vibration Analysis Diagnostics
permalink: /
layout: single
---

## Preface
Have you ever heard an annoying, funky little recurring noise when driving down the highway and simply turned up the radio slightly? Don't disregard that noise! You might accidentally be causing a disservice to the health of your vehicle. A lot of the noises heard are a result of vibrations at different points of a car that are transmitted through the drivetrain, suspention and chassis. These vibrations are always present to some degree, but at certain frequencies get amplified. This would be the part's resonant frequency. We ideally do not want to find the resonant frequencies while in our every day drive, much less hover in them.

Although one could always detect the revolutions per minute (rpm) or speeds at which vibrations feel much stronger by simply glancing at the dash, it's not very intuitive to feel out which harmonics are also amplified at those rpm. According to vibration analysts, these harmonics can reveal to us roughly what part of the car is experiencing issues. Most professional equipment involve thousands of dollars worth sensors that get placed in very specific parts of the vehicle. However, since a lot of these vibrations travel through the entire system, we figured that a more economical way of recording this data would be through our phone accelerometers. We then created our system that takes in accelerometer data and produces a film featuring rolling fast fourier transform (FFT) of this data and a power spectral density (PSD) of the data.

## Record the Vibrations
Our software takes in a very specifically formatted `.csv` file based on `.mat` files. We recommend using the MATLAB Mobile app since it allows us to record a face value sample rate of 100Hz that actually resulted to be 200 Hz (increases our Nyquist frequency to well above 6000 RPM which is rarerly achieved during a normal drive anyway). Before recording the data, make sure to set the sampling speed for the accelerometer to 100Hz (the highest setting in MATLAB Mobile) in the Sampling Parameters bar. The screen should look something like this:

![MATLAB Screen](/media/images/matlab_screen.jpg)

Then, place the phone on the dashboard of the vehicle. We personally placed it on a phone holder that is placed directly on the dashboard with command strips; however, it is best to keep the phone as flat to the dash's surface to avoid accounting for other motions such as the jitter of the dash-phone-holder system.

Once you're ready to go for a drive, press the start button and you're good to go! Just make sure that the phone doesn't go into sleep mode at any point, so try to extend the phone's screen time as long as the intended drive length, if not longer. Just remember to set it back after the experiment to conserve your battery!

Once the data has been saved into a `.mat` file, retrieve the data from the MATLAB cloud and download it to the computer where this software lives. You will need to have MATLAB open to convert the `.mat` file into a `.csv` file. To do this, load the file into the workspace, and simply hit the export button, and export to a `.csv` file. An example of a `.csv` file can be found in the Github repository.

## Analyze the Vibrations
To run our tool, simply run `python main.py` in a terminal of your choice. If you hadn't already, don't forget to make sure you have the dependencies the software takes advantage of. Please refer to the [requirements.txt](/requirements.txt) file enlosing this information. Make sure to be in the repository where the `.csv` file **and** the `main.py` file are. An easy way would be to run the following series of commands, replacing "PATH_TO_DIRECTORY" with the correct path to the directory containing the necessary files:
```
cd PATH_TO_DIRECTORY/
python main.py
```
Running the program may take a little while, but what you will get is effectively a movie showing the rolling FFT, and two images - one for the PSD accros the data, and another for the PSDs of the transmission gears. Depending on how the peaks line up, it may indicate whether the gears are presenting any issues, or otherwise can be a history of gear usage during the ride. To get an accurate PSD result for the gears, you may have to replace them with the specs of your vehicle.

For a more complete demonstration of the results, please refer to our [results](/results/) page.

## Reflections
We acknowledge that this is not a fool proof solution to any car issue in its current state. This is merely a proof of concept that these vibrations can and do contain information about the driving state of the vehicle. Several issues require more than just RPM peaks, but rather need a combination of velocity, and in some cases, knowledge of which gear the car is in. At a given time.

As previously noted, real vibration analyses make sure of very precise sensors that are places in very specific points of the vehicle. They also take advantage of live data collection and are connected to the car's electronics through the OBD2 port, which we were unable to do for this project's scope. Regardless, this software model proves to us that there are definitely correlations between vibrations and car parts, and that vibrations can be used to determine vehicle issues. Further reflections can be found in our [results](/results/) page.