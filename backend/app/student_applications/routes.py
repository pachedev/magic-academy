from flask import jsonify, request, make_response, render_template
from app.student_applications import bp
from app.extensions import db
from app.models.grimorio import Grimorio
from app.models.grimorio_assignment import GrimorioAssignment
from app.models.student_application import StudentApplication
from app.utils import APPLICATION_REQUIRED_FIELDS, MAGIC_AFFINITIES, review_information_received, compare_required_fields, get_random_grimorio

# Consulta todas las solicitudes.
@bp.route('/solicitudes', methods=['GET'])
def get_student_applications():
	try:
		applications = db.session.query(StudentApplication).all()
		applications_data = [sa.json() for sa in applications]
		return jsonify(applications_data), 200
	except Exception as e:
		return make_response(jsonify({'message': 'Ocurrio un error obtener las solicitudes.', 'error': str(e)}), 500)

# Consulta todas las solicitudes y las muestra
@bp.route('/solicitudes/view')
def index():
	try:
		applications = db.session.query(StudentApplication).all()
	except Exception as e:
		applications = []
		print('Error obteniendo las solicitudes: ', e)
	return render_template('student_applications/index.html', applications=applications)

# Procesa las solicitudes de ingreso
@bp.route('/solicitud', methods=['POST'])
def create_student_application():
	try:
		data = request.get_json()
		check_required_fields = compare_required_fields(APPLICATION_REQUIRED_FIELDS, data)
		if check_required_fields:
			errors = []
			magic_affinity = data['magic_affinity']
			for key in data.keys():
				test_value = data[key]
				# Si es el campo de afinidad convierte a minusculas el valor para validar correctamente el valor de la afinidad magica
				if key == 'magic_affinity':
					test_value = test_value.lower()
					if test_value in MAGIC_AFFINITIES:
						magic_affinity = MAGIC_AFFINITIES[test_value]
					else:
						magic_affinity = ''
				if not review_information_received(test_value, APPLICATION_REQUIRED_FIELDS[key]['regex']):
					errors.append(f'El campo {key} no es valido, se esperan {APPLICATION_REQUIRED_FIELDS[key]["description"]}')
			# Valida si ya existe una solicitud con el mismo Identificador
			application = db.session.query(StudentApplication).filter_by(identification=data['identification']).first()
			if not application:
				state = 'rejected'
				if len(errors) == 0:
					state = 'received'
					errors = '\n'.join(errors)
				new_application = StudentApplication(name=data['name'], last_name=data['last_name'], identification=data['identification'], age=data['age'], magic_affinity=magic_affinity, state=state)
				db.session.add(new_application)
				db.session.commit()
				# Crear asiganción de un Grimorio
				if state == 'received':
					# Obtiene los Grimorios de la base de datos
					db_grimorios = db.session.query(Grimorio).all()
					# Armar los arreglos para obtener un Grimorio según una ponderación
					weights = []
					grimorios = []
					for g in db_grimorios:
						grimorio_data = g.simple_json()
						grimorios.append(grimorio_data)
						weights.append(grimorio_data['weight'])
					# Obtiene un Grimorio según una ponderación
					grimorio = get_random_grimorio(grimorios, weights)
					if grimorio:
						new_assignment = GrimorioAssignment(application_id=new_application.application_id, grimorio_id=grimorio['id'])
						db.session.add(new_assignment)
						db.session.commit()
						new_application.assignment_id = new_assignment.assignment_id
						new_application.state = 'assigned'
						new_application.sate = 'assigned'
						db.session.commit()
					return jsonify({
						'id': new_application.application_id,
						'name': new_application.name,
						'last_name': new_application.last_name,
						'identification': new_application.identification,
						'magic_affinity': {'code': new_application.magic_affinity.code, 'value': new_application.magic_affinity.value},
					}), 201
			else:
				return make_response(jsonify({'message': f'Ya existe una solicitud con el identificador: {data["identification"]}.'}), 400)
			return make_response(jsonify({'message': f'Tu solicitud fue rechazada por las siguientes razones: {errors}.'}), 400)
		return make_response(jsonify({'message': 'Los campos Nombre, Apellido, Identificación, Edad y Afinidad Mágica son requeridos.'}), 400)
	except Exception as e:
		return make_response(jsonify({'message': 'Ocurrio un error al crear la solicitud.', 'error': str(e)}), 500)

# Actualiza las solicitudes de ingreso.
@bp.route('/solicitud/<int:application_id>', methods=['PUT'])
def update_student_applications(application_id):
	try:
		application = db.session.query(StudentApplication).filter_by(application_id=application_id).first()
		if application:
			if application.state.code != 'assigned':
				data = request.get_json()
				check_required_fields = compare_required_fields(APPLICATION_REQUIRED_FIELDS, data)
				if check_required_fields:
					errors = []
					magic_affinity = data['magic_affinity']
					for key in data.keys():
						test_value = data[key]
						# Si es el campo de afinidad convierte a minusculas el valor para validar correctamente el valor de la afinidad magica
						if key == 'magic_affinity':
							test_value = test_value.lower()
							if test_value in MAGIC_AFFINITIES:
								magic_affinity = MAGIC_AFFINITIES[test_value]
						if not review_information_received(test_value, APPLICATION_REQUIRED_FIELDS[key]['regex']):
							errors.append(f'El campo {key} no es valido, se esperan {APPLICATION_REQUIRED_FIELDS[key]["description"]}')
					if len(errors) == 0:
						application.name = data['name']
						application.last_name = data['last_name']
						application.last_name = data['last_name']
						application.identification = data['identification']
						application.age = data['age']
						application.state = 'received'
						application.magic_affinity = magic_affinity
						db.session.commit()
						return make_response(jsonify({'application': application.json()}), 200)
				return make_response(jsonify({'message': f'Tu solicitud no fue actualizada por las siguientes razones: {errors}.'}), 400)
			else:
				return make_response(jsonify({'message': f'Tu solicitud no fue actualizada por que ya esta asignada.'}), 400)
		return make_response(jsonify({'message': 'La solicitud de ingreso no existe.'}), 404)
	except Exception as e:
		return make_response(jsonify({'message': 'Ocurrio un error al obtener la solicitud: ', 'error': str(e)}), 500)

# Actualiza el estado de las solicitudes de ingreso.
@bp.route('/solicitud/<int:application_id>/status', methods=['PATCH'])
def update_state_student_applications(application_id):
	try:
		application = db.session.query(StudentApplication).filter_by(application_id=application_id).first()
		if application:
			if application.state.code != 'rejected':
				data = request.get_json()
				errors = []
				if 'state' in data:
					if data['state'] == 'rejected':
						GrimorioAssignment
						assignment = db.session.query(GrimorioAssignment).filter_by(application_id=application.application_id).first()
						if assignment:
							db.session.delete(assignment)
							db.session.commit()
						application.state = data['state']
						db.session.commit()
						return make_response(jsonify({'application': application.json()}), 200)
					else:
						errors.append('Una solicitud solo se puedes cambiar al estado rechazado.')
				else:
					errors.append("El campo status es requerido.")
				errors = "\n".join(errors)
				return make_response(jsonify({'message': f'La solicitud no fue actualizada por las siguientes razones: {errors}'}), 400)
			else:
				return make_response(jsonify({'message': f'La solicitud no fue actualizada por que ya esta cancelada.'}), 400)
		return make_response(jsonify({'message': 'La solicitud de ingreso no existe.'}), 404)
	except Exception as e:
		return make_response(jsonify({'message': 'Ocurrio un error al obtener la solicitud: ', 'error': str(e)}), 500)


# Elimina solicitudes de ingreso.
@bp.route('/solicitud/<int:application_id>', methods=['DELETE'])
def delete_student_applications(application_id):
	try:
		application = db.session.query(StudentApplication).filter_by(application_id=application_id).first()
		if application:
			if not application.assignment_id:
				db.session.delete(application)
				db.session.commit()
				return make_response(jsonify({'message': 'Se ha eliminado la solicitud.'}), 200)
			else:
				return make_response(jsonify({'message': f'La solicitud no fue borrada por que ya cuenta con un Grimorio asignado.'}), 400)
		return make_response(jsonify({'message': 'La solicitud de ingreso no existe.'}), 404)
	except Exception as e:
		return make_response(jsonify({'message': 'Ocurrio un error al obtener la solicitud: ', 'error': str(e)}), 500)