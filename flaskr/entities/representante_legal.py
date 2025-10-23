from .base import BaseEntity
from flaskr.__init__ import db

class RepresentanteLegal(BaseEntity, db.Model):
	__tablename__ = 'representantes'
	
	id			= db.Column(db.Integer, primary_key=True, autoincrement=True)
	proyecto_id = db.Column(db.Integer, db.ForeignKey('projects.id'), unique=False, nullable=False)
	nombre		= db.Column(db.String(128))
	email		= db.Column(db.String(128))
	telefono	= db.Column(db.String(64))
	proyecto	= db.relationship('Project', back_populates='representantes')

	def get_json_fields(self):
		return [
			'id',
			'proyecto_id',
			'nombre',
			'email',
			'telefono',
		]
