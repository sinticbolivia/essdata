from .base import BaseEntity
from flaskr.__init__ import db


class Project(BaseEntity, db.Model):
	__tablename__ = 'projects'
	
	id					= db.Column(db.Integer, primary_key=True, autoincrement=True)
	external_id			= db.Column(db.Integer)
	proyecto_id			= db.Column(db.Integer)
	nombre				= db.Column(db.String(256))
	tecnologia			= db.Column(db.String(128), nullable=False)
	fecha_publicacion	= db.Column(db.DateTime)
	empresa				= db.Column(db.String(128))
	tipo				= db.Column(db.String(128))
	estado				= db.Column(db.String(128))
	region				= db.Column(db.String(128))
	comuna				= db.Column(db.String(128))
	estado_solicitud	= db.Column(db.String(64))
	fecha_recepcion		= db.Column(db.DateTime)
	fecha_estimada_conexion = db.Column(db.DateTime)
	capacidad			= db.Column(db.String(32))
	rca					= db.Column(db.String(128))
	frca				= db.Column(db.DateTime)
	
	representantes		= db.relationship('RepresentanteLegal', back_populates='proyecto', lazy='dynamic')
	coordinadores		= db.relationship('Coordinador', back_populates='proyecto', lazy='dynamic')
	
	'''
	def __init__(self, **kwargs):
		# print("1. Create a new instance of Point.___init___")
		# super(Project, self).__init__(**kwargs)
		# self._serializable = []
		super(BaseEntity, self).__init__()
		super(db.Model, self).__init__(**kwargs)
	'''
		
	def get_json_fields(self):
		return [
			'id',
			'external_id',
			'proyecto_id',
			'nombre',
			'tecnologia',
			'empresa',
			'tipo',
			'estado',
			'region',
			'comuna',
		]
