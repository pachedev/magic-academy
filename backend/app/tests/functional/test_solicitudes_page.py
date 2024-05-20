from app import create_app
from os import environ

def test_solicitudes_page():
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/solicitudes/view' page is requested (GET)
	THEN check that the response is valid
	"""
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.get('/solicitudes/view')
		assert response.status_code == 200
		assert b"Magic Academy" in response.data
		assert b"Inicio" in response.data
		assert b"Solicitudes" in response.data
		assert b"Asignaciones" in response.data
		assert b"Solicitudes de estudiantes" in response.data
		assert b"Solicitudes recibidas" in response.data
		assert b"Copyright" in response.data
		assert b"Subir" in response.data