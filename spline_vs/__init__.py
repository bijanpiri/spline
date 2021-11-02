import os

from flask import Flask, render_template
from . import spline


def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    app.register_blueprint(spline.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
