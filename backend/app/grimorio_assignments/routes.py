from flask import jsonify, make_response, render_template
from app.grimorio_assignments import bp
from app.extensions import db
from app.models.grimorio import Grimorio
from app.models.grimorio_assignment import GrimorioAssignment
from app.models.student_application import StudentApplication
from app.utils import build_response, parse_datetime_to_str

# Consulta todas las asignaciones de Grimorios.
@bp.route('/', methods=['GET'],strict_slashes=False)
def get_assignments():
	try:
		assignments = db.session.query(GrimorioAssignment).all()
		assignments_data = []
		for ga in assignments:
			application = db.session.query(StudentApplication).filter_by(application_id=ga.application_id).first()
			grimorio = db.session.query(Grimorio).filter_by(grimorio_id=ga.grimorio_id).first()
			assignments_data.append({'id': ga.assignment_id, 'application':application.json(), 'grimorio':grimorio.json(), 'created_at':parse_datetime_to_str(ga.created_at)})
		return build_response({'message': 'Solicitudes de ingreso obtenidas exitosamente.', 'assignments': assignments_data}, 200)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error obtener las asignaciones.', 'error': str(e)}, 500)

# Consulta todas las asignaciones de Grimorios y las muestra.
@bp.route('/view',strict_slashes=False)
def index():
	try:
		assignments = db.session.query(GrimorioAssignment).all()
		assignments_data = []
		for ga in assignments:
			application = db.session.query(StudentApplication).filter_by(application_id=ga.application_id).first()
			grimorio = db.session.query(Grimorio).filter_by(grimorio_id=ga.grimorio_id).first()
			assignments_data.append({'id': ga.assignment_id, 'application':application.json(), 'grimorio':grimorio.json(), 'created_at':parse_datetime_to_str(ga.created_at)})
	except Exception as e:
		assignments_data = []
	return render_template('grimorio_assignments/index.html', assignments=assignments_data)
