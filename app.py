from flask import *
from audio_features import *
import os
import numpy as np
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#when called turns the file in sample audio into 8d
def convert_to_8D():
    #load song as time series
    wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features('./out/test.wav')
    #elevate mono signal - in beta until reconstruction is fixed
    #wav_mono_elevated = elevation(wav_mono, tempo, sampling_rate)
    #rotate stereo panning based off elevated signal
    wav = rotate_left_right(wav_mono, wav_stereo, tempo, sampling_rate)
    #save before SoX adds effects
    save_song('./out/effectz.wav', wav, sampling_rate)
    #apply SoX transformer
    #add_effects('./out/in.wav')
    return "Done Conversion"

#wipe the previous songs, had issues when overwriting and webpage not properally reloading
def clear_directories():
    if os.path.exists(APP_ROOT + '/out/test.wav'):
        os.remove(APP_ROOT + '/out/test.wav')
    if os.path.exists(APP_ROOT + '/out/effectz.wav'):
        os.remove(APP_ROOT + '/out/effectz.wav')
    if os.path.exists(APP_ROOT + '/out/in.wav'):
        os.remove(APP_ROOT + '/out/in.wav')
    return "Done Path Clearing"

#homepage
@app.route('/')
def index():
    return render_template('index.html')

#to request to download song to local machine
@app.route('/out/effectz.wav')
def download_file():
    if os.path.exists(APP_ROOT + '/out/effectz.wav'): return send_file(APP_ROOT+ '/out/effectz.wav')
    return " "


#route for when link is submitted
@app.route('/convert', methods=['POST'])
def convert():
    def long_time(url):
        #clear directories of previous songs
        clear_directories()
        #downlaod the audio from the link given
        yield download_from_youtube(url)
        #convert downloaded song in sample audio to 8d and save out
        wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features('./out/test.wav')
        yield "Loaded Song"
        wav = rotate_left_right(wav_mono, wav_stereo, tempo, sampling_rate)
        yield "Rotation"
        save_song('./out/effectz.wav', wav, sampling_rate)
        yield "Saved to Path"
        #add_effects('./out/in.wav')
        yield "Added Reverb"
        #render listening page with audio controller setup to play the file saved by convert to 8d
    return Response(long_time(request.values['url']))

if __name__ == '__main__':
    app.run(debug = True)
