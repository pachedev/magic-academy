from flask import jsonify, make_response
from re import match
from datetime import timedelta
from random import choices

# Campos requeridos en las solicitudes
APPLICATION_REQUIRED_FIELDS = {
	'name': {
		'regex': '^[A-Za-z]{1,20}$',
		'description': 'solo letras, máximo 20 caracteres.',
	},
	'last_name': {
		'regex': '^[A-Za-z]{1,20}$',
		'description': 'solo letras, máximo 20 caracteres.',
	},
	'identification': {
		'regex': '^[A-Za-z0-9]{1,10}$',
		'description': 'números y letras, máximo 10 caracteres.',
	},
	'age': {
		'regex': '^\d{1,2}$',
		'description': 'solo letras, máximo 20 caracteres.',
	},
	'magic_affinity': {
		'regex': '^(darkness|light|fire|water|wind|earth)$',
		'description': 'una única opción entre Oscuridad(darkness), Luz(light), Fuego(fire), Agua(water), Viento(wind) o Tierra(earth).',
	}
}

# Afinidades mágicas validas
MAGIC_AFFINITIES = ['darkness', 'light', 'fire', 'water', 'wind', 'earth']

# Estados permitidos para realizar la actualización de estado en las solicitudes (Aprobar(assigned), Rechazar(rejected))
APPLICATION_STATES = ['assigned', 'rejected']

# Validad la que un valor cumpla con x expresión regular
def review_information_received(value, regular_expression):
	if value:
		if match(regular_expression, str(value)):
			return True
	return False

# Convierte una fecha y hora a un string con el tz de la Ciudad de México
# ya que el servidor de la DB guarda los registros en UTC
def parse_datetime_to_str(dt):
	if dt:
		dt_mexico_city = dt - timedelta(hours=6)
		return dt_mexico_city.strftime("%d/%m/%Y, %H:%M:%S")
	return ""

# Campara si todas la llaves del object1 están object2
def compare_required_fields(object1, object2):
	return set(object1.keys()).issubset(set(object2.keys()))

# Realiza asignación de Grimorios considerando la siguiente ponderación
# En este caso, se han asignado los pesos [10, 8, 6, 4, 1] a las opciones "one_leaf", "two_leaf", "three_leaf", "four_leaf" y "five_leaf", respectivamente.
# Estos pesos indican la probabilidad relativa de seleccionar cada opción.
# Cuanto mayor sea el peso, mayor será la probabilidad de que se seleccione esa opción.
def get_random_grimorio(grimorios, weights, options=1):
	return choices(grimorios, weights=weights, k=options)[0]

# Construye una respuesta estandar para el API
def build_response(body, code=200):
	formatted_body = jsonify(body)
	return make_response(formatted_body, code)
