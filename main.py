import numpy as np
#import scipy as sp
import scipy.io as sio
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip, CompositeAudioClip,AudioFileClip
from moviepy.video.io.bindings import mplfig_to_npimage
import csv
from datetime import datetime as dt, timedelta as td

FILE_NAME = "sensorlog_20221212_144004.csv"
AUDIO_FILE = "sensorlog_20221212_144004.mp4"
GEAR_RATIOS = [3.75,2.41,1.41,1.0,.72]
AXEL_RATIO = 3.31
TIRE_DIAMETER = 84.8/(12*5280) #MILES
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

class mat_movie_maker():
    video_offset = 0
    xl_offset = 0
    total_offset=1

    rollingfft_length = 5

    def __init__(self,_time,data):
        self.data_time = _time
        self.data_xl = data
        self.fig = None
        self.ax = None
        pass

    def calculate_duration(self):
        audioclip = AudioFileClip(AUDIO_FILE)
        new_audioclip = CompositeAudioClip([audioclip])
        self.audio_durarion = new_audioclip.duration
        return self.audio_durarion
        #self._start_time = min(self.data_time)
        #self._end_time = max(self.data_time)
        #out = (self._end_time-self._start_time).total_seconds()
        #return (self._end_time-self._start_time).total_seconds()#-self.rollingfft_length


    def make_movie(self):
        self.generate_psd()
        self.fig, self.ax = plt.subplots()
        #animation.ipython_display(fps = 30, loop = True, autoplay = True)
        audioclip = AudioFileClip(AUDIO_FILE)
        new_audioclip = CompositeAudioClip([audioclip])
        self.audio_durarion = new_audioclip.duration

        animation = VideoClip(self.make_frame, duration =self.audio_durarion)
        animation.audio = new_audioclip
        animation.write_videofile(filename= FILE_NAME+".mp4",fps = 30,codec = "h264")
        pass

    def make_frame(self,time):
        self.ax.clear()
        freqs,absft = self.get_fft_of_time(time)
        self.ax.plot(freqs,absft)
        self.ax.set_xlabel('Frequency (rpm)')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_ylim(0,.25)
        self.ax.set_xlim(0,5500)
        #self.ax.set_ylim(-1.5, 2.5)
        return mplfig_to_npimage(self.fig)
        pass

    def generate_psd(self):
        self.calculate_duration()
        self._start_time = 0#min(self.data_time)

        samplingFrequency = len(times)/self.audio_durarion
        fig, ax = plt.subplots()
        no_g = np.add(self.data_xl,-np.average(self.data_xl))
        px, frpm = ax.psd(no_g,Fs=samplingFrequency*60)
        gear_fs = [np.multiply(frpm,gear) for gear in GEAR_RATIOS]
        ax.set_xlim(0,5500)
        ax.set_xlabel("Frequency (rpm)")
        image_format = 'svg' # e.g .png, .svg, etc.
        image_name = FILE_NAME+'.svg'
        fig.savefig(image_name, format=image_format, dpi=2400)
        image_format = 'png' # e.g .png, .svg, etc.
        image_name = FILE_NAME+'.png'
        fig.savefig(image_name, format=image_format, dpi=600)
        pxrpm = np.multiply(px,60)
        ax.clear()
        for i, gearf in enumerate(gear_fs):
            ax.plot(gearf,pxrpm,label = f"{ordinal(i+1)} gear")
        ax.legend()
        ax.set_xlim(0,4500)
        ax.set_xlabel("engine rpms compared to driveshaft speed")
        ax.set_ylabel("power spectral density (db/rpm")
        image_format = 'svg' # e.g .png, .svg, etc.
        image_name = FILE_NAME+'gears.svg'
        fig.savefig(image_name, format=image_format, dpi=2400)
        image_format = 'png' # e.g .png, .svg, etc.
        image_name = FILE_NAME+'gears.png'
        fig.savefig(image_name, format=image_format, dpi=600)
        pass



    def get_fft_from_time_to_time(self,start_time,end_time):
        (data, times)  = self.get_data_in_time_range(start_time,end_time)
        data = np.add(data,-np.average(self.data_xl))
        avg_sample_int = np.average(np.diff(times))
        samplingFrequency = len(self.data_time)/self.audio_durarion#1/avg_sample_int
        fourierTransform = np.fft.fft(data)/len(data)           # Normalize amplitude
        fourierTransform = fourierTransform[range(int(len(data)/2))] # Exclude sampling frequency 
        tpCount     = len(data)

        values      = np.arange(int(tpCount/2))

        timePeriod  = tpCount/(samplingFrequency*60)

        frequencies = values/timePeriod
        return (frequencies,abs(fourierTransform))

    def get_fft_of_time(self,time):
        s_time = max(0,time-self.rollingfft_length)
        e_time = min(self.calculate_duration(),s_time+self.rollingfft_length)
        s_time = min(s_time,e_time-self.rollingfft_length)
        return self.get_fft_from_time_to_time(s_time,e_time)
        
        pass

    def get_data_in_time_range(self, start_time, end_time):
        psudeo_times = [(self.audio_durarion/len(self.data_time))*i for i,_ in enumerate(self.data_time)]
        indexes = []#index 
        for index, _time in enumerate(psudeo_times):
            sec_from_start = _time#((_time-self._start_time).total_seconds())
            if (start_time <= sec_from_start < end_time):
                indexes.append(index)
        data = [self.data_xl[index]for index in indexes]
        #_time = [(psudeo_times[index]-self._start_time).total_seconds() for index in indexes]
        _time = [psudeo_times[index] for index in indexes]
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

