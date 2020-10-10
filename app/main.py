import json
import uuid

from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    make_response,
)

from .utils import *

def getPercent(number):
    number*= 100
    return "{:.3f}%".format(number)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = str((Path(__file__).parent/Path('.uploaded')).resolve())

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    

@app.route('/incjs', methods=['GET'])
def include_js():
    response = make_response(f"let ajax = {{ fileUpload: {{ url: '{url_for('upload')}'}}}};")
    response.headers['Content-Type'] = 'text/javascript'
    return response


@app.route('/upload', methods=['POST'])
def upload():
    upload_folder = Path(app.config['UPLOAD_FOLDER'])
    if not upload_folder.exists():
        upload_folder.mkdir(parents=True)
    uploaded_files = request.files.getlist('files_up')
    filenames = []
    sim_matrix = []
    for f in uploaded_files:
        if f.filename:
            filenames.append(f.filename)
            f.save(str(f.filename))
    if filenames:
        matrix = check_similarity(filenames)
        for i in range(matrix.shape[0]):
            sim_matrix.append([filenames[i]] + list(map(getPercent, matrix[i])))
        sim_matrix.insert(0, [''] + filenames)

        for f in filenames:
            Path(f).unlink(missing_ok=True)
    return {
        'sim_matrix': sim_matrix,
        'filenames': filenames
    }
