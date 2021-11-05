from json.decoder import JSONDecodeError
from typing import Mapping
from flask import Blueprint, flash, redirect, request, Response, render_template, url_for, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, send_file
import os
from PIL import Image, ImageDraw, UnidentifiedImageError
import io
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import interpolate


bp = Blueprint('spline', __name__, url_prefix='/sp')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = current_app.config['ALLOWED_IMAGE_EXTENSIONS']

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/annotate', methods=['POST'])
def annotate():
    """
        Rest API for to annotate images with spline
        In order to make it work you have to provide t,c,k 
        and image parameters within your POST requests

        Here is an example:

        t = [110,125, 150, 200, 320, 420, 550, 610]
        c = [12, -1, 13,-2, 10]
        k = 2
        image = your_image.jpg

    """

    # Check if Request has image file field
    if 'image' not in request.files:
        return "No image has been uploaded for spline annotation", 400

    image_file: FileStorage = request.files['image']

    if not allowed_file(image_file.filename):
        return "This file extension is not supported.", 400

    form = request.form  # shorter variable

    loss_params_messages = {
        't': 'Knot points not found in your request. Check if the "t" parameter is set.',
        'c': 'No coefficient has been set. Recheck your c parameter',
        'k': 'Degree of spline has not been sent. set the k parameter'
    }

    # Checks if tck parameters are included in request or not
    error_messages = [loss_params_messages[key]
                      for key in loss_params_messages if not key in form]

    if error_messages:
        return "Invalid Request:\n"+"\n".join(error_messages), 400

    buffer = io.BytesIO()

    try:
        k = int(form['k'])
        t = json.loads(form['t'])
        c = json.loads(form['c'])

        with Image.open(image_file) as im:
            draw = ImageDraw.Draw(im)  # draw handle of pillow image library

            # Computing Spline and drawing it on image

            # calculate bspline function with given tck parameters
            # and returns function
            spl = interpolate.BSpline(t, c, k)

            # generates x values in range of t(0) to t(n)
            xx = np.linspace(t[0], t[-1], t[-1]-t[0])
            # evaluate generated x in spline function to generate list of (x,y) tuples
            # we could also use spline evaluation function as shown below :
            # yy = interpolate.splev(xx,(t,c,k))
            yy = spl(xx)
            xy = [(x, y) for x, y in zip(xx, yy)]
            draw.line(xy, fill=200, width=3)

            # Marks knot points on spline:
            ky = [(x, y) for x, y in zip(t, spl(t))]
            xy0 = np.array(ky) - 4  # knot points circle start
            xy1 = np.array(ky) + 4  # knot points circle end
            for p1, p2 in zip(xy0, xy1):
                draw.ellipse([tuple(p1), tuple(p2)],
                             fill=(0, 220, 20), outline=255)

            # Saves images with drawn spline to buffer in order to make response
            im.save(buffer, 'JPEG')
            # Reset buffer head to the start to make its content readable by send_file
            buffer.seek(0)

    except UnidentifiedImageError:
        return "Bad image file or corrupted image.", 400
    except JSONDecodeError as jde:
        return f'Error parsing request parameters {jde}', 400
    except ValueError as ve:
        return f'Value Error: {ve}', 400
    
    return send_file(buffer, environ=request.environ, mimetype="image/jpeg")
