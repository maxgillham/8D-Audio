from flask import *
from audio_features import *
import os
import numpy as np
import json

app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_AUTO_RELOAD = True



def convert_to_8D():
    os.chdir(APP_ROOT + '/sample_audio')
    file_name = os.listdir()
    wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features(file_name[0])
    wav_mono_elevated = elevation(wav_mono, tempo, sampling_rate)
    wav = rotate_left_right(wav_mono_elevated, wav_stereo, tempo, sampling_rate)
    os.chdir(APP_ROOT + '/static')
    save_song('in.wav', wav, sampling_rate)
    add_effects('in.wav')
    return 

def clear_directories():
    if os.path.exists(APP_ROOT + '/sample_audio/test.wav'):
        os.remove(APP_ROOT + '/sample_audio/test.wav')
    if os.path.exists(APP_ROOT + '/static/effectz.wav'):
        os.remove(APP_ROOT + '/static/effectz.wav')
    if os.path.exists(APP_ROOT + '/static/in.wav'):
        os.remove(APP_ROOT + '/static/in.wav')
    return

def maybe_make_dir():
    files = os.listdir()
    if 'sample_audio' not in files: os.mkdir('sample_audio')
    if 'static' not in files: os.mkdir('static')
    return

#homepage
@app.route('/')
def index():
    os.chdir(APP_ROOT)
    return render_template('index.html')

@app.route('/static/effectz.wav')
def download_file():
    return send_file(APP_ROOT+ '/static/effectz.wav')

@app.route('/download_by_link', methods=['POST'])
def download_by_link():
    clear_directories()
    download_from_youtube(request.values['link'])
    convert_to_8D()
    return render_template('listen.html')


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
