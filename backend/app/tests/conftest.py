import os
import pytest

from app import create_app
from app.extensions import db, Base
from app.models.grimorio import Grimorio
from config import TestingConfig


# --------
# Fixtures
# --------

@pytest.fixture
def test_client():
	# Set the Testing configuration prior to creating the Flask application
	os.environ['CONFIG_TYPE'] = 'config.TestingConfig'

	flask_app = create_app(TestingConfig)

	# Create a test client using the Flask application configured for testing
	with flask_app.test_client() as testing_client:
		# Establish an application context
		with flask_app.app_context():
			# Crea las tablas en la base de datos antes de la primer solicitud al servicio
			Base.metadata.create_all(bind=db.engine)
			yield testing_client  # this is where the testing happens!

@pytest.fixture
def init_database(test_client):
	# Create the database and the database table
	db.create_all()

	# Insert Grimorio data
	grimorio_1 = Grimorio(name='Aguilas Plateadas', clover_type='one_leaf', rarity='common', weight=10)
	grimorio_2 = Grimorio(name='Amanecer Dorado', clover_type='three_leaf', rarity='unusual', weight=8)
	grimorio_3 = Grimorio(name='Mantis Verdes', clover_type='five_leaf', rarity='very_rare', weight=6)
	db.session.add(grimorio_1)
	db.session.add(grimorio_2)
	db.session.add(grimorio_3)

	# Commit the changes for the books
	db.session.commit()

	yield  # this is where the testing happens!

	db.drop_all()

@pytest.fixture
def cli_test_client():
	# Set the Testing configuration prior to creating the Flask application
	os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
	flask_app = create_app()

	runner = flask_app.test_cli_runner()

	yield runner  # this is where the testing happens!
