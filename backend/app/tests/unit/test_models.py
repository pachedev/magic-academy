from app.models.grimorio import Grimorio
from app.models.grimorio_assignment import GrimorioAssignment
from app.models.student_application import StudentApplication

def test_new_grimorio():
	"""
	GIVEN a Grimorio model
	WHEN a new Grimorio is created
	THEN check the name, clover_type, rarity, weight and image fields are defined correctly
	"""
	grimorio = Grimorio(name='Aguilas Plateadas', clover_type='five_leaf', rarity='very_rare', weight=1)
	assert grimorio.name == 'Aguilas Plateadas'
	assert grimorio.clover_type == 'five_leaf'
	assert grimorio.rarity == 'very_rare'
	assert grimorio.weight == 1
	assert grimorio.image == None

def test_new_student_application():
	"""
	GIVEN a StudentApplication model
	WHEN a new StudentApplication is created
	THEN check the application_id and grimorio_id fields are defined correctly
	"""
	student_application = StudentApplication(name='Harry', last_name='Potter', identification='1234567890', age=17, magic_affinity='light', state='received')
	assert student_application.name == 'Harry'
	assert student_application.last_name == 'Potter'
	assert student_application.identification == '1234567890'
	assert student_application.age == 17
	assert student_application.magic_affinity == 'light'
	assert student_application.state == 'received'

def test_new_grimorio_assignment():
	"""
	GIVEN a GrimorioAssignment model
	WHEN a new GrimorioAssignment is created
	THEN check the application_id and grimorio_id fields are defined correctly
	"""
	assignment = GrimorioAssignment(application_id=1, grimorio_id=1)
	assert assignment.application_id == 1
	assert assignment.grimorio_id == 1
