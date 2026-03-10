from flask import Blueprint, render_template
from flask_login import current_user

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def landing():
    return render_template('landing.html', user=current_user)

@pages_bp.route('/dashboard')
def index():
    return render_template('index.html', user=current_user)

@pages_bp.route('/map')
def map_view():
    return render_template('map.html', user=current_user)

@pages_bp.route('/favourites')
def favourites():
    return render_template('favourites.html', user=current_user)