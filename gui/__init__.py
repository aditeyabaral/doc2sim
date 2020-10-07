import json

from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    url_for
)

import gui.filebrowser


here = Path(__file__)


def create_app(sim_callback=None, here=here):
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        similarity_matrix = []
        messages = []
        if request.method == 'POST' and sim_callback is not None:
            form_filelist = json.loads(request.form.get('filelist'))
            filenames = []
            for f in form_filelist:
                if Path(f.get('filename')).exists():
                    filenames.append(f.get('filename'))
                else:
                    messages.append(f"<strong>{f.get('filename')}</strong> doesn't exists!!!")
            if filenames:
                similarity_matrix = sim_callback(filenames)
        return render_template('index.html', similarity_matrix=similarity_matrix, here=str(here.parent), messages=messages)
    
    @app.route('/filelist', methods=['POST'])
    def file_browser():
        form_path = request.form.get('filepath')
        folder_action = request.form.get('folderaction')
        p = Path(form_path)
        if p.is_dir():
            if folder_action == 'up':
                p = p.parent
            current_folder = str(p.resolve())
            return {
                'data': filebrowser.browse(current_folder),
                'current_folder': current_folder,
            }
        return {'data': [], 'current_folder': ''}
    
    @app.route('/incjs', methods=['GET'])
    def include_js():
        return f"let config = {{ fileBrowserURL: \'{url_for('file_browser')}\', localPath: \'{str(here.parent)}\' }}"
    
    return app
