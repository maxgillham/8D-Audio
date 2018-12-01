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
    #l = elevation(wav[0,:], tempo, sampling_rate)
    #r = elevation(wav[1,:], tempo, sampling_rate)
    #y = np.stack((l,r))
    os.chdir(APP_ROOT + '/static')
<<<<<<< HEAD
    save_song('test.wav', y, sampling_rate)
    add_effects('test.wav')
    return
=======
    save_song('in.wav', wav, sampling_rate)
    add_effects('in.wav')
    return 
>>>>>>> 2aecd565318a9afe13ae40c4907649114e63fe38

def clear_directories():
    os.chdir(APP_ROOT + '/sample_audio')
    files = os.listdir()
    for file in files:
        os.remove(file)
    os.chdir(APP_ROOT + '/static')
    files = os.listdir()
    for file in files:
        print(file)
        os.remove(file)
    os.chdir(APP_ROOT)
    return

def maybe_make_dir():
    files = os.listdir()
    if 'sample_audio' not in files: os.mkdir('sample_audio')
    if 'static' not in files: os.mkdir('static')
    return

#homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print('\nHIT UPLOAD')
    target = os.path.join(APP_ROOT, 'sample_audio/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        filename = 'test.wav'
        destination = '/'.join([target, filename])
        file.save(destination)

    convert_to_8D()
 
    
    #render_template('listen.html')
    return render_template('index.html')

@app.route('/reset')
def reset():
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
<<<<<<< HEAD
    #maybe_make_dir()
    TEMPLATES_AUTO_RELOAD = True
=======
    maybe_make_dir()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
>>>>>>> 2aecd565318a9afe13ae40c4907649114e63fe38
    app.run(debug = True)
