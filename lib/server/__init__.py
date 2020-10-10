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

import doc2sim


def to_fixed(number, precision):
    s = str(number)
    i = s.find('.')
    return ''.join((s[:i+1], s[i+1:i+precision+1].ljust(precision, '0')))


#def create_app():
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
    local_filenames = []
    filenames = []
    sim_matrix = []
    for f in uploaded_files:
        if f.filename:
            uuid_filename = upload_folder/Path(str(uuid.uuid4()))
            local_filenames.append(str(uuid_filename))
            filenames.append(f.filename)
            f.save(str(uuid_filename))
    if filenames:
        matrix = doc2sim.check_similarity(local_filenames)
        # print('[DEBUG]', matrix)
        for i in range(matrix.shape[0]):
            sim_matrix.append([filenames[i]] + list(map(lambda x: to_fixed(x, 3), matrix[i])))
        sim_matrix.insert(0, [''] + filenames)
        # Delete uploaded files
        for f in local_filenames:
            Path(f).unlink(missing_ok=True)
    return {
        'sim_matrix': sim_matrix,
        'filenames': filenames
    }
    
    #return app
