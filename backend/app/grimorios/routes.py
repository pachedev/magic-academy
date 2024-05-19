from flask import jsonify, make_response
from app.grimorios import bp
from app.extensions import db
from app.models.grimorio import Grimorio

@bp.route('/', methods=['GET'])
def get_grimorios():
	try:
		grimorios = db.session.query(Grimorio).all()
		grimorios_data = [g.json() for g in grimorios]
		return jsonify(grimorios_data), 200
	except Exception as e:
		return make_response(jsonify({'message': 'Ocurrio un error obtener los grimorios.', 'error': str(e)}), 500)