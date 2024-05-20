from app import create_app
from os import environ
import json
from app.extensions import db, Base

from pathlib import Path

# get the resources folder in the tests folder
resources = Path(__file__).parent / "functional"

def test_get_grimorios():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.get('/grimorios')
		assert response.status_code == 200
		res_json = json.loads(response.data.decode('utf-8'))
		message = res_json.get("message")
		grimorios = res_json.get("grimorios")
		assert type(message) is str
		assert type(grimorios) is list

def test_get_asignaciones():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.get('/asignaciones')
		assert response.status_code == 200
		res_json = json.loads(response.data.decode('utf-8'))
		message = res_json.get("message")
		asignaciones = res_json.get("assignments")
		assert type(message) is str
		assert type(asignaciones) is list

def test_get_solicitudes():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.get('/solicitudes')
		res_json = json.loads(response.data.decode('utf-8'))
		print("res_json: ",res_json)
		assert response.status_code == 200
		message = res_json.get("message")
		applications = res_json.get("applications")
		assert type(message) is str
		assert type(applications) is list

def test_solicitud_create():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.post('/solicitud', json={
			"name": "Lord",
			"last_name": "Voldemort",
			"identification": "F123456789",
			"age": 50,
			"magic_affinity": "darkness"
		})
		assert response.status_code == 201
		res_json = json.loads(response.data.decode('utf-8'))
		message = res_json.get("message")
		assert type(message) is str

def test_solicitud_update():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.put('/solicitud/2', json={
			"name": "Hermione",
			"last_name": "Granger",
			"identification": "B123456789",
			"age": 17,
			"magic_affinity": "light"
		})
		assert response.status_code == 200
		res_json = json.loads(response.data.decode('utf-8'))
		message = res_json.get("message")
		application = res_json.get("application")
		assert type(message) is str
		assert type(application) is dict

def test_solicitud_update_status():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.patch('/solicitud/1/status', json={
			"status": "assigned",
		})
		assert response.status_code == 200
		res_json = json.loads(response.data.decode('utf-8'))
		message = res_json.get("message")
		application = res_json.get("application")
		assert type(message) is str
		assert type(application) is dict

def test_solicitud_delete():
	# Set the Testing configuration prior to creating the Flask application
	environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as test_client:
		response = test_client.delete('/solicitud/100')
		assert response.status_code == 404
		res_json = json.loads(response.data.decode('utf-8'))
		message = res_json.get("message")
		assert type(message) is str