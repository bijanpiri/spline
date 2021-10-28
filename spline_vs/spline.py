from flask import Blueprint, render_template



bp = Blueprint('spline',__name__,url_prefix='/sp')


@bp.route('/')
def index():
    return render_template('spline/spline.html')

@bp.route('/annotate')
def annotate():
    
    pass    

