from .base import BaseEntity
from flaskr.__init__ import db

class Parameter(BaseEntity, db.Model):

	__tablename__ = 'parameters'
	
	id		= db.Column(db.Integer, primary_key=True, autoincrement=True)
	key		= db.Column(db.String(256))
	value	= db.Column(db.Text())

	def get_json_fields(self):
		return [
			'id',
			'key',
			'value',
		]
