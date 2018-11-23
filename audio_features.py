import librosa
import os
import sox
import matplotlib.pyplot as plt
import numpy as np

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
def rotate_left_right(wav_mono, wav_stereo, tempo, sampling_rate):
    length = wav_mono.shape[0]
    #sample value that indicates transition
    end_of_beat = int((tempo / 120) * sampling_rate)
    #this is the rate the amplitude will increase by over
    down_value = .15
    amplitude_down = np.linspace(1, down_value, 2*end_of_beat)
    amplitude_up = np.linspace(down_value, 1, 2*end_of_beat)
    #make a seccond up and down that move differently
    amplitude_down_slower = np.logspace(1, down_value, 8*end_of_beat)
    amplitude_up_slower = np.logspace(down_value, 1, 8*end_of_beat)

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
    tfm.reverb(reverberance=50)
    tfm.treble(gain_db=5, slope=.3)
    tfm.bass(gain_db=5, slope=0.3)
    tfm.build(input, 'effectz.wav')
    return

'''
Just using this to compare plots of stereo channels for
wav file generated in here and one produced by youtube channel
'''
def plot_stereo_balance(wav_1, wav_2):
    #make wav contents into numpy arrays
    wav_1 = np.array(wav_1)
    wav_2 = np.array(wav_2)
    #make x values for plotting, likely the same size
    x_1 = np.arange(0, wav_1.shape[1])
    x_2 = np.arange(0, wav_2.shape[1])
    #plot each channel
    plt.subplot(121)
    plt.scatter(x_1, wav_1[0, :], marker='.', c='b')
    plt.scatter(x_1, wav_1[1, :], marker='.', c='g')
    plt.subplot(122)
    plt.scatter(x_2, wav_2[0, :], marker='.', c='r')
    plt.scatter(x_2, wav_2[1, :], marker='.', c='k')
    plt.show()
    return

'''
Method of sin wav to figure out some channel positioning for left, right, up and down.
I would not reccomend listening to this for fun, its very, very annoying
'''
def make_sigletone():
    return np.column_stack((.5*np.sin(.05*np.linspace(0, 1000000, 1000000)), .5*np.sin(.05*np.linspace(0, 1000000, 1000000)))).T
