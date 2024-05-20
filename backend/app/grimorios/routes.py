from app.grimorios import bp
from app.extensions import db
from app.models.grimorio import Grimorio
from app.utils import build_response


@bp.route('/', methods=['GET'], strict_slashes=False)
def get_grimorios():
	try:
		grimorios = db.session.query(Grimorio).all()
		grimorios_data = [g.json() for g in grimorios]
		return build_response({'message': 'Grimorios obtenidos exitosamente', 'grimorios': grimorios_data}, 200)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error obtener los grimorios.', 'error': str(e)}, 500)