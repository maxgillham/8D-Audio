import librosa
import os
import sox
import numpy as np
import youtube_dl

from scipy.signal import butter, lfilter

#global path variable for loading and saving
path = os.getcwd()

'''
This method takes file names and returns the wav file as time
series, sampling rate and tempo
'''
def song_features(file_name):

    #waveform and sampleing rate
    wav_mono, sampling_rate = librosa.load(file_name)

    #wavform and sampling rate, need wav stereo
    wav_stereo, sampling_rate = librosa.load(file_name, mono=False)

    #tempo and beatframes
    tempo, beat_frames = librosa.beat.beat_track(y=wav_stereo[0], sr=sampling_rate)

    return wav_mono, wav_stereo, sampling_rate, tempo, beat_frames

'''
Just saves the time series as a wav file
'''
def save_song(name, wav, sampling_rate):
    librosa.output.write_wav(name, wav, sampling_rate)
    return

'''
Change the volumes of the left and right ears
to go up and down, opposite of eachother. Has a maintain
period after rising chanel.  Transitions are made every
4 beats. Returns as stereo.
'''
def rotate_left_right(wav_mono, wav_stereo, tempo, sampling_rate):
    length = wav_mono.shape[0]
    #sample value that indicates transition
    end_of_beat = int((tempo / 120) * sampling_rate)
    #this is the rate the amplitude will increase by over
    down_value = .15
    amplitude_down = np.linspace(1, down_value, 2*end_of_beat)
    amplitude_up = np.linspace(down_value, 1, 2*end_of_beat)
    #make a seccond up and down that move differently
    amplitude_down_slower = np.linspace(1, down_value, 8*end_of_beat)
    amplitude_up_slower = np.linspace(down_value, 1, 8*end_of_beat)

    #flag to determine if sound should be maintained
    left_up = False
    right_up = False
    left_maintain = False
    right_maintain = True
    i = 0
    while i < length - 8*end_of_beat:
        fast = np.random.choice([True, False])
        #if left channel flagged to go up
        if left_up:
            if fast:
                #turn left up and turn right down, with faster ramp
                wav_stereo[0, i:i+(2*end_of_beat)] = wav_mono[i:i+(2*end_of_beat)]*amplitude_up
                wav_stereo[1, i:i+(2*end_of_beat)] = wav_mono[i:i+(2*end_of_beat)]*amplitude_down
                #set left maintain flag
                left_up = False
                left_maintain = True
                i += (2 * end_of_beat)
            else:
                #turn left up and right down, with slower ramp
                wav_stereo[0, i:i+(8*end_of_beat)] = wav_mono[i:i+(8*end_of_beat)]*amplitude_up_slower
                wav_stereo[1, i:i+(8*end_of_beat)] = wav_mono[i:i+(8*end_of_beat)]*amplitude_down_slower
                #set left maintain flag
                left_up = False
                left_maintain = True
                i += (8 * end_of_beat)

        #if right channel flagged to go up
        elif right_up:
            if fast:
                #turn up right and turn down left
                wav_stereo[1, i:i+(2*end_of_beat)] = wav_mono[i:i+(2*end_of_beat)]*amplitude_up
                wav_stereo[0, i:i+(2*end_of_beat)] = wav_mono[i:i+(2*end_of_beat)]*amplitude_down
                right_up = False
                right_maintain = True
                i += (2 * end_of_beat)
            else:
                #turn up right and turn down left
                wav_stereo[1, i:i+(8*end_of_beat)] = wav_mono[i:i+(8*end_of_beat)]*amplitude_up_slower
                wav_stereo[0, i:i+(8*end_of_beat)] = wav_mono[i:i+(8*end_of_beat)]*amplitude_down_slower
                right_up = False
                right_maintain = True
                i += (8 * end_of_beat)
        #if left channel flagged to stay constant
        elif left_maintain:
            wav_stereo[0, i:i+end_of_beat] = wav_mono[i:i+end_of_beat]
            wav_stereo[1, i:i+end_of_beat] = wav_mono[i:i+end_of_beat]*down_value
            right_up = True
            left_maintain = False
            i += end_of_beat

        #maintain right channel for 1 bar
        elif right_maintain:
            wav_stereo[1, i:i + end_of_beat] = wav_mono[i:i + end_of_beat]
            wav_stereo[0, i:i + end_of_beat] = wav_mono[i:i+end_of_beat]*down_value
            right_maintain = False
            left_up = True
            i += end_of_beat

    wav_stereo[0, (length//(8*end_of_beat))*(8*end_of_beat):] *= 0
    wav_stereo[1, (length//(8*end_of_beat))*(8*end_of_beat):] *= 0
    return wav_stereo

'''
This method uses the wrapper class pysox for Sox to add some effects to the song
'''
def add_effects(input):
    tfm = sox.Transformer()
    tfm.reverb(reverberance=25)
    tfm.treble(gain_db=5, slope=.3)
    tfm.bass(gain_db=5, slope=0.3)
    tfm.build(input, './out/effectz.wav')
    return

'''
Method of sin wav to figure out some channel positioning for left, right, up and down.
I would not reccomend listening to this for fun, its very, very annoying
'''
def make_sigletone():
    return np.column_stack((.5*np.sin(.05*np.linspace(0, 1000000, 1000000)), .5*np.sin(.05*np.linspace(0, 1000000, 1000000)))).T

'''
These methods concern applying high and low passfilters to resemble a sense
of audio elevation
'''
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def elevation(wav_mono, tempo, sampling_rate):
    length = len(wav_mono)
    end_of_beat = int((tempo / 120) * sampling_rate)*2

    order = 6
    fs = 30.0
    i = 1
    y = np.empty(0)

    low = True

    while i < length:
        #low pass filter with cutoff decreasing
        cutoff = 10
        y = np.append(y, butter_lowpass_filter(wav_mono[i:i+end_of_beat], cutoff, fs, order))
        cutoff = 9.25
        y = np.append(y, butter_lowpass_filter(wav_mono[i+end_of_beat-1:i+2*end_of_beat], cutoff, fs, order))
        cutoff = 8.75
        y = np.append(y, butter_lowpass_filter(wav_mono[i+2*end_of_beat-1:i+3*end_of_beat], cutoff, fs, order))
        cutoff = 8
        y = np.append(y, butter_lowpass_filter(wav_mono[i+3*end_of_beat-1:i+4*end_of_beat], cutoff, fs, order))

        i += 4*end_of_beat

        #high pass filter with cutoff increasing
        cutoff = 8
        y = np.append(y, butter_highpass_filter(wav_mono[i-1:i+end_of_beat], cutoff, fs, order))
        cutoff = 8.75
        y = np.append(y, butter_highpass_filter(wav_mono[i+end_of_beat-1:i+2*end_of_beat], cutoff, fs, order))
        cutoff = 9.25
        y = np.append(y, butter_highpass_filter(wav_mono[i+2*end_of_beat-1:i+3*end_of_beat], cutoff, fs, order))
        cutoff = 10
        y = np.append(y, butter_highpass_filter(wav_mono[i+3*end_of_beat-1:i+4*end_of_beat], cutoff, fs, order))

        i += 4*end_of_beat

    return y

'''
Util to download the audio for a given youtube url
'''
def download_from_youtube(url):
    ydl_opts = {
        'outtmpl': 'out/test.wav',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "Done Download"
