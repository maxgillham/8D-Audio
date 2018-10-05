import librosa
import os
import matplotlib.pyplot as plt
import numpy as np

from math import *

#global path variable for loading and saving
path = os.getcwd()

'''
This method takes file names and returns the wav file as time
series, sampling rate and tempo
'''
def song_features(file_name):

    #waveform and sampleing rate
    wav_mono, sampling_rate = librosa.load(file_name, duration=120)

    #wavform and sampling rate, need wav stereo
    wav_stereo, sampling_rate = librosa.load(file_name, mono=False, duration=120)

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
def rotate_left_right(wav_mono, wav_stereo, sampling_rate, tempo):
    length = wav_mono.shape[0]
    #sample value that indicates transition
    end_of_bar = int((4/(tempo/60))*sampling_rate)
    #this is the rate the amplitude will increase by over
    amplitude_down = np.linspace(1, .2, 4*end_of_bar)
    amplitude_up = np.linspace(.2, 1, 4*end_of_bar)
    down_value = .2
    #flag to determine if sound should be maintained
    left_up = True
    right_up = False
    left_maintain = False
    right_maintain = False
    i = 0
    while i < (length//(4*end_of_bar))*(4*end_of_bar):
    #for i in range(0, (length//(2*end_of_bar))*(2*end_of_bar), end_of_bar):
        #if left channel flagged to go up
        if left_up:
            #turn left up and turn right down
            wav_stereo[0, i:i+(4*end_of_bar)] = wav_mono[i:i+(4*end_of_bar)]*amplitude_up
            wav_stereo[1, i:i+(4*end_of_bar)] = wav_mono[i:i+(4*end_of_bar)]*amplitude_down
            #set left maintain flag
            left_maintain = True
            left_up = False
            i += (4 * end_of_bar)


        #if right channel flagged to go up
        elif right_up:
            #turn up right and turn down left
            wav_stereo[1, i:i+(4*end_of_bar)] = wav_mono[i:i+(4*end_of_bar)]*amplitude_up
            wav_stereo[0, i:i+(4*end_of_bar)] = wav_mono[i:i+(4*end_of_bar)]*amplitude_down
            right_maintain = True
            right_up = False
            i += (4 * end_of_bar)

        #if left channel flagged to stay constant
        elif left_maintain:
            wav_stereo[0, i:i+end_of_bar] = wav_mono[i:i+end_of_bar]
            wav_stereo[1,i:i+end_of_bar] = wav_mono[i:i+end_of_bar]*down_value
            left_maintain = False
            right_up = True
            i += end_of_bar

        #maintain right channel for 1 bar
        elif right_maintain:
            wav_stereo[1, i:i + end_of_bar] = wav_mono[i:i + end_of_bar]
            wav_stereo[0, i:i + end_of_bar] = wav_mono[i:i+end_of_bar]*down_value
            right_maintain = False
            left_up = True
            i += end_of_bar
    return wav_stereo

'''
Just using this to compare plots of stereo channels for
wav file generated in here and one produced by youtube channel
'''
def plot_stereo_balance(wav_1, wav_2):
    #make wav contents into numpy arrays
    wav_1 = np.array(wav_1)
    wav_2 = np.array(wav_2)
    #make x values for plotting, likely the same size
    x_1 = np.arange(0,wav_1.shape[1])
    x_2 = np.arange(0,wav_2.shape[1])
    #plot each channel
    plt.subplot(121)
    plt.scatter(x_1, wav_1[0,:], marker='.', c='b')
    plt.scatter(x_1, wav_1[1,:], marker='.', c='g')
    plt.subplot(122)
    plt.scatter(x_2, wav_2[0,:], marker='.', c='r')
    plt.scatter(x_2, wav_2[1,:], marker='.', c='k')
    plt.show()
    return

if __name__ == '__main__':
    os.chdir(path + '/sample_audio')
    #file_name = os.listdir()

    wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features('magic.wav')

    wav = rotate_left_right(wav_mono, wav_stereo, sampling_rate, tempo)

    os.chdir(path + '/sample_output')
    save_song('new_magic.wav', wav, sampling_rate)
