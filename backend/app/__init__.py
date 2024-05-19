from flask import Flask
from flask_cors import CORS

from config import Config
from app.extensions import db, Base

from time import sleep

def create_app(config_class=Config):
	app = Flask(__name__)
	CORS(app)
	app.config.from_object(config_class)

	# Import modules
	from app.models.grimorio import Grimorio
	from app.models.grimorio_assignment import GrimorioAssignment
	from app.models.student_application import StudentApplication

	# Initialize Flask extensions
	db.init_app(app)

	# Blueprints
	from app.main import bp as main_bp
	app.register_blueprint(main_bp)
	# Grimorios
	from app.grimorios import bp as grimorios_bp
	app.register_blueprint(grimorios_bp, url_prefix='/grimorios')
	# Grimorio assignments
	from app.grimorio_assignments import bp as grimorio_assignments_bp
	app.register_blueprint(grimorio_assignments_bp, url_prefix='/asignaciones')
	# Student applications
	from app.student_applications import bp as student_applications_bp
	app.register_blueprint(student_applications_bp, url_prefix='/')

	@app.route('/test')
	def test_page():
		return '<h1>Testing the Magic Academy</h1>'

	# Crea las tablas en la base de datos antes de la primer solicitud al servicio
	@app.before_request
	def init_db():
		with app.app_context():
			Base.metadata.create_all(bind=db.engine)

	return app
