import json

from pathlib import Path

from flask import (
    Flask,
    render_template,
    request
)

here = Path(__file__)

def create_app(sim_callback=None, here=here):
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        similarity_matrix = []
        if request.method == 'POST' and sim_callback is not None:
            filenames = json.loads(request.form.get('filelist'))
            similarity_matrix = sim_callback(filenames)
        return render_template('index.html', similarity_matrix=similarity_matrix, here=str(here.parent))
    
    return app
