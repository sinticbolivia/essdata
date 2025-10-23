# -*- coding: utf-8 -*-
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)
from flaskr.common.functions import *
from flaskr.factory import Factory
from flaskr.entities import Project
from datetime import datetime
from sqlalchemy import and_, or_, not_
#from ..sea import * as sea
import flaskr.sea as sea

bp = Blueprint('sea_api', __name__, url_prefix = '/api/sea')

@bp.route('/matches/<id>')
def get_matches(id):
	prj = Project.query.get(id)
	
	try:
		if prj is None:
			raise Exception('Proyecto no encontrado')
		dataframe = sea.search_keywords()
		keyword = None
		if 'SAE' in prj.nombre or 'almacenamiento' in prj.nombre.lower():
			keyword = 'almacenamiento'
		elif 'BESS' in prj.nombre:
			keyword = 'bess'
		if keyword is None:
			raise Exception('El proyecto no contiene ningun palabra de busqueda')
		print('MATCH KEYWORD: ', keyword)
		
		matches = dataframe[dataframe['nombre'].str.contains(keyword, case=False)]
		return matches.to_json(orient='table')
	except Exception as e:
		res = make_response({error: str(e)}, 500)
		res.mimetype = 'application/json'
		return res
