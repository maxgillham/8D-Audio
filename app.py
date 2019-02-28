from flask import Flask, render_template, Response, request, send_file
from audio_features import song_features, download_from_youtube, rotate_left_right, save_song, add_effects
import os
import numpy as np
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


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
        save_song('./out/in.wav', wav, sampling_rate)
        yield "Saved to Path"
        add_effects('./out/in.wav')
        yield "Added Reverb"
    return Response(long_time(request.values['url']))

if __name__ == '__main__':
    app.run(debug = True)
