from flask import *
from audio_features import *
import os
import numpy as np
import json

app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_AUTO_RELOAD = True


#when called turns the file in sample audio into 8d
def convert_to_8D():
    #os.chdir(APP_ROOT + '/sample_audio')
    #file_name = os.listdir()
    #load song as time series
    wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features('./static/test.wav')
    #elevate mono signal
    wav_mono_elevated = elevation(wav_mono, tempo, sampling_rate)
    #rotate stereo panning based off elevated signal
    wav = rotate_left_right(wav_mono_elevated, wav_stereo, tempo, sampling_rate)
    #os.chdir(APP_ROOT + '/static')
    #save before SoX adds effects
    save_song('./static/in.wav', wav, sampling_rate)
    #apply SoX transformer
    add_effects('./static/in.wav')
    return

#wipe the previous songs, had issues when overwriting and webpage not properally reloading
def clear_directories():
    if os.path.exists(APP_ROOT + '/static/test.wav'):
        os.remove(APP_ROOT + '/static/test.wav')
    if os.path.exists(APP_ROOT + '/static/effectz.wav'):
        os.remove(APP_ROOT + '/static/effectz.wav')
    if os.path.exists(APP_ROOT + '/static/in.wav'):
        os.remove(APP_ROOT + '/static/in.wav')
    return

def maybe_make_dir():
    files = os.listdir()
    #if 'sample_audio' not in files: os.mkdir('sample_audio')
    if 'static' not in files: os.mkdir('static')
    return

#homepage
@app.route('/')
def index():
    os.chdir(APP_ROOT)
    return render_template('index.html')

#to request to download song to local machine
@app.route('/static/effectz.wav')
def download_file():
    return send_file(APP_ROOT+ '/static/effectz.wav')

#route for when link is submitted
@app.route('/download_by_link', methods=['POST'])
def download_by_link():
    #clear directories of previous songs
    clear_directories()
    os.chdir(APP_ROOT)
    #downlaod the audio from the link given
    download_from_youtube(request.values['link'])
    #convert downloaded song in sample audio to 8d and save in static
    convert_to_8D()
    #render listening page with audio controller setup to play the file saved by convert to 8d
    return render_template('listen.html')


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
