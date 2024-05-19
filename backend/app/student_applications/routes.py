from flask import request, render_template
from app.student_applications import bp
from app.extensions import db
from app.models.grimorio import Grimorio
from app.models.grimorio_assignment import GrimorioAssignment
from app.models.student_application import StudentApplication
from app.utils import build_response, APPLICATION_REQUIRED_FIELDS, APPLICATION_STATES, review_information_received, compare_required_fields, get_random_grimorio

# Consulta todas las solicitudes.
@bp.route('/solicitudes', methods=['GET'])
def get_student_applications():
	try:
		applications = db.session.query(StudentApplication).all()
		applications_data = [sa.json() for sa in applications]
		return build_response({'message': 'Solicitudes obtenidas exitosamente.', 'applications': applications_data}, 200)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error obtener las solicitudes.', 'error': str(e)}, 500)

# Consulta todas las solicitudes y las muestra
@bp.route('/solicitudes/view')
def index():
	try:
		applications = db.session.query(StudentApplication).all()
	except Exception as e:
		applications = []
	return render_template('student_applications/index.html', applications=applications)

# Procesa las solicitudes de ingreso
@bp.route('/solicitud', methods=['POST'])
def create_student_application():
	try:
		data = request.get_json()
		check_required_fields = compare_required_fields(APPLICATION_REQUIRED_FIELDS, data)
		# Valida que los campos requeridos se incluyan en la petición
		if check_required_fields:
			errors = []
			magic_affinity = data['magic_affinity']
			# Valida para cada uno de los campos el si cumplen con las expresiones regulares
			for key in data.keys():
				if not review_information_received(data[key], APPLICATION_REQUIRED_FIELDS[key]['regex']):
					errors.append(f'El campo {key} no es valido, se esperan {APPLICATION_REQUIRED_FIELDS[key]["description"]}')
					if key == 'magic_affinity':
						magic_affinity = ''
			# Valida si ya existe una solicitud con el mismo Identificador
			application = db.session.query(StudentApplication).filter_by(identification=data['identification']).first()
			if not application:
				# Estado por default de la solicitud en caso de no complir todos los requerimientos
				state = 'rejected'
				# Si no hay errores, cambia el estado por default a solicitud recibida
				if len(errors) == 0:
					state = 'received'
				# Crear la solicitud
				new_application = StudentApplication(name=data['name'], last_name=data['last_name'], identification=data['identification'], age=data['age'], magic_affinity=magic_affinity, state=state)
				db.session.add(new_application)
				db.session.commit()
				# Crear asiganción de un Grimorio, si se cumplieron todos los requerimientos
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
						# Crea la asignación
						new_assignment = GrimorioAssignment(application_id=new_application.application_id, grimorio_id=grimorio['id'])
						db.session.add(new_assignment)
						db.session.commit()
						# Asocia la asignación a la solicitud de ingreso
						new_application.assignment_id = new_assignment.assignment_id
						new_application.state = 'assigned'
						db.session.commit()
					return build_response({'message': 'Se registro la solicitud correctamente.', 'application': new_application.json()}, 201)
				else:
					errors = '\n'.join(errors)
					return build_response({'message': f'Tu solicitud fue rechazada por las siguientes razones: {errors}.'}, 400)
			else:
				return build_response({'message': f'Ya existe una solicitud con el identificador: {data["identification"]}.'}, 400)
		return build_response({'message': 'Los campos Nombre, Apellido, Identificación, Edad y Afinidad Mágica son requeridos.'}, 400)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error al crear la solicitud.', 'error': str(e)}, 500)

# Actualiza las solicitudes de ingreso.
@bp.route('/solicitud/<int:application_id>', methods=['PUT'])
def update_student_applications(application_id):
	try:
		application = db.session.query(StudentApplication).filter_by(application_id=application_id).first()
		if application:
			if application.state.code != 'assigned':
				data = request.get_json()
				check_required_fields = compare_required_fields(APPLICATION_REQUIRED_FIELDS, data)
				errors = []
				if check_required_fields:
					magic_affinity = data['magic_affinity']
					# Valida para cada uno de los campos el si cumplen con las expresiones regulares
					for key in data.keys():
						if not review_information_received(data[key], APPLICATION_REQUIRED_FIELDS[key]['regex']):
							errors.append(f'El campo {key} no es valido, se esperan {APPLICATION_REQUIRED_FIELDS[key]["description"]}')
							if key == 'magic_affinity':
								magic_affinity = ''
					if len(errors) == 0:
						# Valida si ya existe otra solicitud con el mismo Identificador
						existing_application = db.session.query(StudentApplication).filter(StudentApplication.identification == data['identification'], StudentApplication.application_id != application_id).first()
						if not existing_application:
							application.name = data['name']
							application.last_name = data['last_name']
							application.identification = data['identification']
							application.age = data['age']
							application.state = 'received'
							application.magic_affinity = magic_affinity
							db.session.commit()
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
								# Crea la asignación
								new_assignment = GrimorioAssignment(application_id=application.application_id, grimorio_id=grimorio['id'])
								db.session.add(new_assignment)
								db.session.commit()
								# Asocia la asignación a la solicitud de ingreso
								application.assignment_id = new_assignment.assignment_id
								application.state = 'assigned'
								db.session.commit()
							return build_response({'message': 'Se actualizo la solicitud exitosamente.', 'application': application.json()}, 200)
						else:
							return build_response({'message': f'Tu solicitud no fue actualizada por que el Identificador {data["identification"]} ya fue usado.'}, 400)
				errors = '\n'.join(errors)
				return build_response({'message': f'Tu solicitud no fue actualizada por las siguientes razones: {errors}'}, 400)
			else:
				return build_response({'message': f'Tu solicitud no fue actualizada por que ya esta asignada.'}, 400)
		return build_response({'message': 'La solicitud de ingreso no existe.'}, 404)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error al obtener la solicitud: ', 'error': str(e)}, 500)

# Actualiza el estado de las solicitudes de ingreso.
@bp.route('/solicitud/<int:application_id>/status', methods=['PATCH'])
def update_state_student_applications(application_id):
	try:
		application = db.session.query(StudentApplication).filter_by(application_id=application_id).first()
		if application:
			errors = []
			data = request.get_json()
			if 'status' in data:
				if data['status'] in APPLICATION_STATES:
					if application.state.code != data['status']:
						# Actualiza el status de la solicitud
						application.assignment_id = None
						application.state = data['status']
						db.session.commit()
						# Realiza los procedimientos para eliminar o asignar el grimorio a una solicitud
						existing_assignment = db.session.query(GrimorioAssignment).filter_by(application_id=application_id).first()
						if data['status'] == 'rejected':
							# Si tiene una asignación la elimina
							if existing_assignment:
								db.session.delete(existing_assignment)
								db.session.commit()
						elif data['status'] == 'assigned':
							# Si no tiene una asignación la crear
							existing_assignment = db.session.query(GrimorioAssignment).filter_by(application_id=application_id).first()
							if not existing_assignment:
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
									# Crea la asignación
									new_assignment = GrimorioAssignment(application_id=application_id, grimorio_id=grimorio['id'])
									db.session.add(new_assignment)
									db.session.commit()
									# Asocia la asignación a la solicitud de ingreso
									application.assignment_id = new_assignment.assignment_id
									db.session.commit()
						return build_response({'message': 'Se actualizo el status de la solicitud de ingreso exitosamente.', 'application': application.json()}, 200)
					else:
						errors.append("El campo status no puede ser igual al status actual de la solicitud de ingreso.")
				else:
					errors.append("El campo status no es valido.")
			else:
				errors.append("El campo status es requerido.")
			errors = '\n'.join(errors)
			return build_response({'message': f'El estado de la solicitud de ingreso no fue actualizada por las siguientes razones: {errors}'}, 400)
		return build_response({'message': 'La solicitud de ingreso no existe.'}, 404)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error al obtener la solicitud: ', 'error': str(e)}, 500)

# Elimina solicitudes de ingreso.
@bp.route('/solicitud/<int:application_id>', methods=['DELETE'])
def delete_student_applications(application_id):
	try:
		application = db.session.query(StudentApplication).filter_by(application_id=application_id).first()
		if application:
			if not application.assignment_id:
				db.session.delete(application)
				db.session.commit()
			else:
				assignment = db.session.query(StudentApplication).filter_by(assignment_id=application.assignment_id).first()
				db.session.delete(application)
				db.session.commit()
				if assignment:
					db.session.delete(assignment)
					db.session.commit()
			return build_response({'message': 'Se ha eliminado la solicitud de ingreso.'}, 200)
		return build_response({'message': 'La solicitud de ingreso no existe.'}, 404)
	except Exception as e:
		return build_response({'message': 'Ocurrio un error al obtener la solicitud: ', 'error': str(e)}, 500)
