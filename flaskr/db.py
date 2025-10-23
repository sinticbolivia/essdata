import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#@with_appcontext
def load_entities():
	from .entities import project
	# from .entities import lead
	# from .entities import form
	
@click.command('init-db')
@with_appcontext
def init_db_command():
	load_entities()
	
	from flaskr.__init__ import db
	
	print('init_db_command', db)
	migrate = Migrate(current_app, db)
	db.create_all()
	db.session.commit()
	click.echo('Base de datos inicializada con exito!!!')
	
def init_commands(app):
	#app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
