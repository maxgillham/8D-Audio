from flask import *
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#homepage
@app.route('/')
def index():
   return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'songs/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".wav") or (ext == ".mp3"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/static/')
def download_file(filename):
    return send_file('/static/effectz.wav', filename)






if __name__ == '__main__':
   app.run(debug = True)
