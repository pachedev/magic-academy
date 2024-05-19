from flask import render_template, jsonify
from app.main import bp
from app.extensions import db
from app.models.grimorio import Grimorio

@bp.route('/')
def index():
	try:
		grimorios = db.session.query(Grimorio).all()
	except Exception as e:
		grimorios = []
		print('Error obteniendo el catálogo de grimorios: ', e)
	return render_template('index.html', grimorios=grimorios)
