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

bp = Blueprint('projects_api', __name__, url_prefix = '/api/projects')

@bp.route('/<id>/assign', methods=['POST'])
def assign_match(id):
	prj = Project.query.get(id)
	
	try:
		if prj is None:
			raise Exception('Proyecto no encontrado')
		data = request.get_json()
		print(data)
		prj.rca = data.get('estado')
		prj.frca = datetime.strptime( data.get('fecha_plazo_evaluacion'), '%d/%m/%Y' )
		dbh = Factory.get_db()
		dbh.session.commit()
		
		return prj.dict()
		
	except Exception as e:
		res = make_response({'error': str(e)}, 500)
		res.mimetype = 'application/json'
		return res
