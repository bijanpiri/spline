from typing import Mapping
from flask import Blueprint, flash, redirect, request, Response, render_template, url_for, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, send_file
import os
from PIL import Image
import io
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import interpolate


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
        return  "No image has been uploaded for spline annotation", 400

    image_file = request.files['image']
    # image_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
    #                           secure_filename(image_file.filename))

    form = request.form

    loss_params_messages = {
        't': 'Knot points not found in your request. Check if the "t" parameter is set.',
        'c': 'No coefficient has been set. Recheck your c parameter',
        'k': 'Degree of spline has not been sent. set the k parameter'
    }

    error_messages = [loss_params_messages[key]
                      for key in loss_params_messages if not key in form]

    if error_messages:
        return "Invalid Request:\n"+"\n".join(error_messages),400
    # image_file.save(image_path)

    # reads image from uploaded by form using provided flask's FileStorage
    img = plt.imread(image_file)

    plt.imshow(img)

    k = int(form['k'])
    # t = np.arange(6)
    t = json.loads(form['t'])
    c = json.loads(form['c'])

    spl = interpolate.BSpline(t, c, k)

    # intervals =[np.arange(a,b+.1,.1) for a,b in zip(t[0:-1],t[1:])]

    # for xx in intervals:
    #     plt.plot(xx, spl(xx))

    xx = np.arange(t[0], t[-1]+.1, .1)
    # xx= np.linspace(0,len(c)//2-k,100)
    plt.plot(xx, spl(xx), 'r')
    # plt.plot(xx, interpolate.splev(xx, (t, c, k)), 'g')
    plt.plot(t, spl(t), 'og')
    # plt.axis('off')
    # plt.show()

    buffer = io.BytesIO()

    plt.savefig(buffer, bbox_inches='tight')
    # with Image.open(image_file) as im:
    #     im = im.rotate(90)
    #     # im.save(image_path)

    #     im.save(buffer, "JPEG")
    buffer.seek(0)

    return send_file(buffer, environ=request.environ, mimetype="image/jpeg")
