from flask import *
from audio_features import song_features, rotate_left_right, add_effects, save_song
import os


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def convert_to_8D():
    os.chdir(APP_ROOT + '/sample_audio')
    file_name = os.listdir()

    wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features(file_name[0])
    wav = rotate_left_right(wav_mono, wav_stereo, tempo, sampling_rate)

    os.chdir(APP_ROOT + '/sample_output')
    save_song('in_1.wav', wav, sampling_rate)
    add_effects('in_1.wav')
    return


#homepage
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'sample_audio/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        filename = file.filename
        destination = '/'.join([target, filename])
        file.save(destination)
    convert_to_8D()
    return render_template('index.html')


@app.route('/sample_output/')
def download_file():
    return send_file('/sample_output/effectz.wav')

if __name__ == '__main__':
   app.run(debug = True)
