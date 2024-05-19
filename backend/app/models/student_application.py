from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy_utils import ChoiceType
from app.utils import parse_datetime_to_str
from app.extensions import Base

class StudentApplication(Base):
	__tablename__ = 'student_application'
	STATES = [
		('received', 'Recibida'),
		('assigned', 'Asignada'),
		('rejected', 'Rechazada')
	]
	MAGICAL_AFFINITIES = [
		('darkness', 'Oscuridad'),
		('light', 'Luz'),
		('fire', 'Fuego'),
		('water', 'Agua'),
		('wind', 'Viento'),
		('earth', 'Tierra')
	]
	application_id = Column(Integer, primary_key=True)
	name = Column(String(20), nullable=False)
	last_name = Column(String(20), nullable=False)
	identification = Column(String(10), nullable=False)
	age = Column(Integer, nullable=False)
	magic_affinity = Column(ChoiceType(MAGICAL_AFFINITIES), nullable=True)
	state = Column(ChoiceType(STATES), default='received')
	assignment_id = Column(Integer, ForeignKey('grimorio_assignment.assignment_id'), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
	updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

	def __repr__(self):
		return f'<StudentApplication "{self.application_id}">'

	def json(self):
		return {'id': self.application_id, 'name': self.name, 'last_name': self.last_name, 'identification': self.identification, 'age': self.age, 'magic_affinity': {'code': self.magic_affinity.code, 'value': self.magic_affinity.value}, 'state': {'code': self.state.code, 'value': self.state.value}, 'assignment_id': self.assignment_id, 'created_at': parse_datetime_to_str(self.created_at), 'updated_at': parse_datetime_to_str(self.updated_at)}
