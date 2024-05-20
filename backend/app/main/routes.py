from flask import render_template
from app.main import bp
from app.extensions import db
from app.models.grimorio import Grimorio

@bp.route('/',strict_slashes=False)
def index():
	try:
		grimorios = db.session.query(Grimorio).all()
	except Exception as e:
		grimorios = []
	return render_template('index.html', grimorios=grimorios)