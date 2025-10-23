import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flaskr.factory import Factory
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True, static_folder='static')
	
	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)
	
	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
		
	# db = SQLAlchemy(app)
	db.init_app(app)
	migrate.init_app(app, db)
	
	from .db import init_commands
	init_commands(app)
	Factory.set_db(db)
	
	# import filters
	from .common import filters
	filters.register(app)
	
	from .controllers import PanelController
	from .controllers import CommonController
	from .controllers import ApiSaeController
	from .controllers import ApiProjectsController
	
	app.register_blueprint(CommonController.bp)
	app.register_blueprint(PanelController.bp)
	app.register_blueprint(ApiSaeController.bp)
	app.register_blueprint(ApiProjectsController.bp)
	
	app.add_url_rule('/', endpoint='index')
	
	return app
