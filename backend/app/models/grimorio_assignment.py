from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from app.utils import parse_datetime_to_str
from app.extensions import Base

class GrimorioAssignment(Base):
	__tablename__ = 'grimorio_assignment'
	assignment_id = Column(Integer, primary_key=True)
	application_id = Column(Integer, ForeignKey('student_application.application_id'), nullable=True)
	grimorio_id = Column(Integer, ForeignKey('grimorio.grimorio_id'), nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

	def __repr__(self):
		return f'<GrimorioAssignment "{self.assignment_id}">'

	def json(self):
		return {'id': self.assignment_id, 'application_id': self.application_id, 'grimorio_id': self.grimorio_id, 'created_at': parse_datetime_to_str(self.created_at)}