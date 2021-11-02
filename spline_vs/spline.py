from typing import Mapping
from flask import Blueprint, flash, redirect, request, Response, render_template, url_for, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, send_file
import os
from PIL import Image
import io

bp = Blueprint('spline', __name__, url_prefix='/sp')


@bp.route('/')
def index():
    print(url_for('static', filename='style.css'))
    return render_template('spline/spline.html')


@bp.route('/annotate', methods=['POST'])
def annotate():
    """
        Rest API for to annotate images with spline
        :param image:

    """

    # Check if Request has image file field
    if not 'image' in request.files:
        # flash("No image has been uploaded for spline annotation")
        # return redirect(request.url)
        return {
            'response': "No image has been uploaded for spline annotation"
        }, 400

    image_file: FileStorage = request.files['image']
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                              secure_filename(image_file.filename))


    buffer = io.BytesIO()

    with Image.open(image_file) as im:
        im = im.rotate(90)
        # im.save(image_path)

        im.save(buffer, "JPEG")
        buffer.seek(0)


    return send_file(buffer, environ=request.environ, mimetype="image/jpeg")
