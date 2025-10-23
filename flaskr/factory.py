from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

class Factory:
	data = {}
	
	@staticmethod
	def set_db(db):
		Factory.data['dbh'] = db
		
	def get_db(app=None):
		'''
		if 'db' not in g:
			g.db = SQLAlchemy(app if app is not None else current_app)
			
		return g.db
		'''
		if 'dbh' in Factory.data:
			return Factory.data.get('dbh')
			
		return None
