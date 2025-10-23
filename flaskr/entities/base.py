from flask_sqlalchemy import SQLAlchemy
from flaskr import factory
import json
from datetime import datetime 
from flaskr.__init__ import db
from abc import ABC,abstractmethod
# print('BaseEntity', db)

class BaseEntity:
	deleted					= db.Column(db.SmallInteger, default=0)
	last_modification_date 	= db.Column(db.DateTime, default=datetime.utcnow)
	creation_date			= db.Column(db.DateTime, default=datetime.utcnow)
	

	def bind(self, data):
		
		for key in data:
			setattr(self, key, data[key])

	@abstractmethod
	def get_json_fields(self):
		return []
		
	def dict(self):
		data = {}
		#for attr in dir(self):
		for attr in self.get_json_fields():
			if attr[0] == '_':
				continue
			obj_attr = getattr(self, attr)
			if callable( obj_attr ):
				continue
			if str(type(obj_attr)) == "<type 'classobj'>" and callable(obj_attr, 'json'):
				data[attr] = obj_attr.json()
			else:
				data[attr] = getattr(self, attr)
			
		print('data', self.get_json_fields())
		return data
		
	def json(self):
		return json.dumps(self.dict())
		
	def to_json(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)
		
