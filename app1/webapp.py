from flask import Blueprint
from flask import render_template
server_bp = Blueprint('main', __name__)

@server_bp.route('/')
def index():
    return render_template('index.html', title='Home Page')
