import librosa
import os

from math import *

#global path variable for loading and saving
path = os.getcwd()

'''
This method takes file names and returns the wav file as time
series, sampling rate and tempo
'''
def song_features(file_name):
    #wavform and sampling rate
    wav, sampling_rate = librosa.load(file_name, mono=False, duration=20)

    #tempo and beatframes
    tempo, beat_frames = librosa.beat.beat_track(y=wav[0], sr=sampling_rate)

    return wav, sampling_rate, tempo
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
def rotate_left_and_right(wav, sampling_rate):
    #need to change time series for values 0 to length
    length = wav.shape[1]
    #manipulating amplitude by sin function for left channel and cos for right
    for i in range(length):
        wav[0, i] = wav[:, i]/(5*sin(i/(sampling_rate*pi/2))+10)
        wav[1, i] = wav[:, i]/(5*cos(i/(sampling_rate*pi/2) + sampling_rate/4)+10)
    return wav

if __name__ == '__main__':
    os.chdir(path + '/sample_audio')
    file_name = os.listdir()
    for file in file_name:
        wav, sampling_rate, tempo = song_features(file)
    os.chdir(path + '/sample_output')
    wav = rotate_left_and_right(wav, sampling_rate)
    save_song('yay_for_dsp_and_python.wav', wav, sampling_rate)
