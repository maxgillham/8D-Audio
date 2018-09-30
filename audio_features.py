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
        wav_stereo[0, i] = wav_mono[i]/(6*sin(i/(sampling_rate*pi/2))+10)
        wav_stereo[1, i] = wav_mono[i]/(6*cos(i/(sampling_rate*pi/2) + sampling_rate)+10)
    return wav_stereo

if __name__ == '__main__':
    os.chdir(path + '/sample_audio')
    file_name = os.listdir()
    for file in file_name:
        wav_mono, wav_stereo, sampling_rate, tempo = song_features(file)
    os.chdir(path + '/sample_output')
    wav = rotate_left_and_right(wav_mono, wav_stereo, sampling_rate)
    save_song('yay_for_dsp_and_python.wav', wav, sampling_rate)
