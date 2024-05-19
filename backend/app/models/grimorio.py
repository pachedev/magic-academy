from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy_utils import ChoiceType, URLType
from app.utils import parse_datetime_to_str
from sqlalchemy import event, DDL
from app.extensions import Base

class Grimorio(Base):
	__tablename__ = 'grimorio'
	TYPES = [
		('one_leaf', 'Una hoja'),
		('two_leaf', 'Dos hojas'),
		('three_leaf', 'Tres hojas'),
		('four_leaf', 'Cuatro hojas'),
		('five_leaf', 'Cinco hojas')
	]
	RARITIES = [
		('common', 'Común'),
		('uncommon', 'Poco habitual'),
		('unusual', 'Inusual'),
		('very_rare', 'Muy raro')
	]
	grimorio_id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	clover_type = Column(ChoiceType(TYPES), nullable=False)
	rarity = Column(ChoiceType(RARITIES), nullable=False)
	weight = Column(Integer, nullable=False)
	image = Column(URLType, nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

	def __repr__(self):
		return f'<Grimorio "{self.name}">'

	def json(self):
		return {'id': self.grimorio_id, 'name': self.name, 'clover_type': {'code': self.clover_type.code, 'value': self.clover_type.value}, 'rarity': {'code': self.rarity.code, 'value': self.rarity.value}, 'image': self.image, 'created_at': parse_datetime_to_str(self.created_at)}

	def simple_json(self):
		return {'id': self.grimorio_id, 'name': self.name, 'clover_type': self.clover_type.code, 'rarity': self.rarity.code, 'weight': self.weight}

# Inicializa los valores del catálogo de Grimorios, despues de crear la tabla correspondiente en la base de datos
event.listen(Grimorio.__table__, 'after_create', DDL(""" INSERT INTO grimorio (name, clover_type, rarity, weight, image) VALUES 
	('Grimorio de una hoja', 'one_leaf', 'common', 10, 'https://raw.githubusercontent.com/pachedev/magic-academy/main/images/grimorios/one_leaf.png'),
	('Grimorio de dos hojas', 'two_leaf', 'common', 8, 'https://raw.githubusercontent.com/pachedev/magic-academy/main/images/grimorios/two_leaf.png'),
	('Grimorio de tres hojas', 'three_leaf', 'uncommon', 6, 'https://raw.githubusercontent.com/pachedev/magic-academy/main/images/grimorios/three_leaf.png'),
	('Grimorio de cuatro hojas', 'four_leaf', 'unusual', 4, 'https://raw.githubusercontent.com/pachedev/magic-academy/main/images/grimorios/four_leaf.png'),
	('Grimorio de cinco hojas', 'five_leaf', 'very_rare', 1, 'https://raw.githubusercontent.com/pachedev/magic-academy/main/images/grimorios/five_leaf.png') """))