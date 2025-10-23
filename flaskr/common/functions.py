import os
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import jinja2
#from jinja2 import Template, FileSystemLoader
#from jinja2.environment import Environment
#env = Environment()
#env.loader = FileSystemLoader('.')

def is_admin():
	# current_app.blueprints[request.blueprint]
	return True
	
def get_tpl_basepath(is_admin=False):
	basepath = '{0}/{1}'.format(
		'frontend' if is_admin == False else 'admin', 
		current_app.config['TPL_NAME'],
	)
	
	return basepath

def get_asset_path(filename, is_admin=False):
	assetfile = '{0}/{1}'.format(
		current_app.config['TPL_NAME'] if is_admin == False else current_app.config['ADMIN_TPL_NAME'],
		filename
	)
	return assetfile
	#return url_for('static', filename=filename)
	
def render_tpl(template, **kwargs):
	
	basepath = get_tpl_basepath(is_admin=is_admin())
	
	templateFile = '{0}/{1}'.format(
		basepath,
		template
	)
	print('basepath: ', basepath)
	print('templateFile: ', templateFile)
	return render_template(templateFile, **kwargs)

def set_jinja_tpl_path():
	tpl_path = get_tpl_basepath(is_admin=is_admin())
	
	template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates/' + tpl_path + '/')
	print('jinja2 template dir: ', template_dir)
	jinja_env = jinja2.Environment(
		loader=jinja2.FileSystemLoader([template_dir]), 
		# loader=jinja2.PackageLoader('flaskr', 'templates/' + tpl_path),
		autoescape = True
	)
	print('jinja_env: ', jinja_env)
