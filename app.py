from flask import *
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


@app.route('/static/')
def download_file(filename):
    return send_file('/static/effectz.wav', filename)

@app.route('/')
def index():
   return render_template('index.html')




if __name__ == '__main__':
   app.run(debug = True)
