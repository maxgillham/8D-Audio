import librosa
import os
import matplotlib.pyplot as plt

from math import *

#global path variable for loading and saving
path = os.getcwd()

'''
This method takes file names and returns the wav file as time
series, sampling rate and tempo
'''
def song_features(file_name):

    #waveform and sampleing rate
    wav_mono, sampling_rate = librosa.load(file_name, duration=40)

    #wavform and sampling rate, need wav stereo
    wav_stereo, sampling_rate = librosa.load(file_name, mono=False, duration=40)

    #tempo and beatframes
    tempo, beat_frames = librosa.beat.beat_track(y=wav_stereo[0], sr=sampling_rate)

    return wav_mono, wav_stereo, sampling_rate, tempo

'''
Just saves the time series as a wav file
'''
def save_song(name, wav, sampling_rate):
    librosa.output.write_wav(name, wav, sampling_rate)
    return

'''
Change the volumes of the left and right ears
to go up and down, opposite of eachother
'''
def rotate_left_and_right(wav_mono, wav_stereo, sampling_rate):
    #need to change time series for values 0 to length
    length = wav_mono.shape[0]
    #manipulating amplitude by sin function for left channel and cos for right
    for i in range(length):
        wav_stereo[0, i] = wav_mono[i]/(6*sin(i/(sampling_rate*pi/4))+10)
        wav_stereo[1, i] = wav_mono[i]/(6*sin(i/(sampling_rate*pi/4)+sampling_rate*pi/2)+10)
    return wav_stereo


def plot_stereo_balance(wav_1, wav_2):
    length = len(wav_1[0])
    y_left_1 = []
    y_left_2 = []
    y_right_1 = []
    y_right_2 = []
    x = []
    for i in range(length):
        x.append(i)
        y_left_1.append(wav_1[0, i])
        y_right_1.append(wav_1[1, i])
        y_left_2.append(wav_2[0, i])
        y_right_2.append(wav_2[1, i])
    plt.subplot(121)
    plt.scatter(x, y_left_1, marker='.', c='b')
    plt.scatter(x, y_right_1, marker='.', c='g')
    plt.subplot(122)
    plt.scatter(x, y_left_2, marker='.', c='r')
    plt.scatter(x, y_right_2, marker='.', c='k')
    plt.show()
    return

if __name__ == '__main__':
    os.chdir(path + '/sample_audio')
    #file_name = os.listdir()

    wav_mono_1, wav_stereo_1, sampling_rate_1, tempo_1 = song_features('sweaty.wav')
    wav_1 = rotate_left_and_right(wav_mono_1, wav_stereo_1, sampling_rate_1)

    wav_mono_2, wav_stereo_2, sampling_rate_2, tempo_2 = song_features('sweaty_compare.wav')

    plot_stereo_balance(wav_1, wav_stereo_2)
    #os.chdir(path + '/sample_output')
    #save_song('yay_for_sweat.wav', wav, sampling_rate)
