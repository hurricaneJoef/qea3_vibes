import numpy as np
#import scipy as sp
import scipy.io as sio
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import csv
from datetime import datetime as dt, timedelta as td

FILE_NAME = "sensorlog_20221212_144004.csv"

class mat_movie_maker():
    video_offset = 0
    xl_offset = 0
    total_offset=1

    rollingfft_length = 1

    def __init__(self,_time,data):
        self.data_time = _time
        self.data_xl = data
        self.fig = None
        self.ax = None
        pass

    def calculate_duration(self):
        self._start_time = min(self.data_time)
        self._end_time = max(self.data_time)
        return (self._end_time-self._start_time).total_seconds()-self.rollingfft_length


    def make_movie(self):
        self.fig, self.ax = plt.subplots()
        animation = VideoClip(self.make_frame, duration = self.calculate_duration())
        #animation.ipython_display(fps = 30, loop = True, autoplay = True)
        animation.write_videofile(filename= FILE_NAME+".avi",fps = 30,codec = "mpeg4")
        pass

    def make_frame(self,time):
        self.ax.clear()
        freqs,absft = self.get_fft_of_time(time)
        self.ax.plot(freqs,absft)
        self.ax.set_xlabel('Frequency')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_ylim(0,.2)
        #self.ax.set_ylim(-1.5, 2.5)
        return mplfig_to_npimage(self.fig)
        pass

    def get_fft_of_time(self,time):
        (data, times)  = self.get_data_in_time_range(time,time+self.rollingfft_length)
        avg_sample_int = np.average(np.diff(times))
        samplingFrequency = 1/avg_sample_int
        fourierTransform = np.fft.fft(data)/len(data)           # Normalize amplitude
        fourierTransform = fourierTransform[range(int(len(data)/2))] # Exclude sampling frequency 
        tpCount     = len(data)

        values      = np.arange(int(tpCount/2))

        timePeriod  = tpCount/samplingFrequency

        frequencies = values/timePeriod
        return (frequencies[1:-1],abs(fourierTransform[1:-1]))
        pass

    def get_data_in_time_range(self, start_time, end_time):
        indexes = []#index 
        for index, _time in enumerate(self.data_time):
            sec_from_start = ((_time-self._start_time).total_seconds())
            if (start_time <= sec_from_start < end_time):
                indexes.append(index)
                if index > 5320:
                    None
        data = [self.data_xl[index]for index in indexes]
        _time = [(self.data_time[index]-self._start_time).total_seconds() for index in indexes]
        return (data,_time)
MONTHS = {
    "Jan":"01",
    "Feb":"02",
    "Mar":"03",
    "Apr":"04",
    "May":"05",
    "Jun":"06",
    "Jul":"07",
    "Aug":"08",
    "Sep":"09",
    "Oct":"10",
    "Nov":"11",
    "Dec":"12"
}
if __name__ == "__main__":
    timedata = []
    times = []
    data = []
    with open(FILE_NAME) as f:
        reader = csv.reader(f,delimiter="\t")
        for row in reader:
            w = row[0].replace("'","")
            for month, numb in MONTHS.items():
                if month in w:
                    w  = w.replace(month,numb)
            #print(w)
            #'01-12-2022 16:55:07.757'
            a = w.split(' ')
            d = a[0].split('-')
            t = a[1].split(':')
            ms = t[2].split('.')
            time = dt(year=int(d[2]),month=int(d[1]),day=int(d[0]),hour=int(t[0]),minute=int(t[1]),second=int(ms[0]),microsecond=int(ms[1])*1000)
            x = float(row[1])
            y = float(row[2])
            z = float(row[3])
            mag = float(np.sqrt(x**2+y**2+z**2))
            times.append(time)
            data.append(mag)
            timedata.append((time,mag))

    mm = mat_movie_maker(times[0:-1],data[0:-1])
    mm.make_movie()

    None

