# -*- coding: utf-8 -*-
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flaskr.common.functions import *
from flaskr.factory import Factory
from flaskr.entities import Project, Coordinador, RepresentanteLegal
from datetime import datetime
from sqlalchemy import and_, or_, not_

bp = Blueprint('panel', __name__)

@bp.route('/')
def index():
	# return 'Hello'
	# return render_template('index.html', app=current_app)
	data = {
		'app': current_app,
		'title': 'Inicio'
	}
	return render_tpl('index.html', **data)


@bp.route('/proyectos')
def proyectos():
	keyword = request.args.get('keyword', '')
	page = int(str(request.args.get('page', '1')))
	dbh = Factory.get_db()
	pagination = None
	
	if keyword:
		pagination = dbh.paginate(
			dbh.Select(Project).filter(
				or_(
					Project.nombre.ilike(f'%{keyword}%'),
					Project.empresa.ilike(f'%{keyword}%'),
					Project.estado_solicitud.ilike(f'%{keyword}%'),
					Project.region.ilike(f'%{keyword}%'),
					Project.capacidad.ilike(f'%{keyword}%'),
				)
				
			).order_by(Project.creation_date), 
			page=page, per_page=50
		)
	else:
		pagination = dbh.paginate(dbh.Select(Project).order_by(Project.creation_date), page=page, per_page=50)
	data = {
		'app': current_app,
		'title': 'Proyectos',
		'pagination': pagination,
		'endpoint': 'panel.proyectos',
		'keyword': keyword
	}
	
	return render_tpl('proyectos.html', **data)

@bp.route('/proyectos/<id>/coordinadores')
def coordinadores(id):
	project = Project.query.get(id)
	
	if project is None:
		return {
			data: None
		}, 404, {'Content-type': 'application/json'}
		
	print(project.coordinadores.all())
	
	# return {'data': jsonify([prj.dict() for prj in project.coordinadores.all()]) if len(project.coordinadores.all()) > 0 else []}
	return [prj.dict() for prj in project.coordinadores.all()] if len(project.coordinadores.all()) > 0 else []
	
@bp.route('/proyectos/<id>/representantes')
def representantes(id):
	print('ID', id);
	project = Project.query.get(id)
	# print(project.json())
	if project is None:
		return {
			data: None
		}, 404, {'Content-type': 'application/json'}
		
	# return {'data': jsonify([prj.dict() for prj in project.representantes.all()]) if len(project.representantes.all()) > 0 else [] } #.json()
	return [prj.dict() for prj in project.representantes.all()] if len(project.representantes.all()) > 0 else []
	
@bp.route('/proyectos/extraer')
def obtener_proyectos():
	import flaskr.process as process
	
	dbh = Factory.get_db()
	data = process.get_json()
	matches = process.get_matches(data)
	print(matches)
	for proyecto in matches:
		
		external_id = proyecto.get('id', 0)
		prj = Project.query.filter_by(external_id=external_id).first()
		if prj is not None:
			print('found', external_id)
			prj.estado_solicitud = proyecto.get('estado_solicitud')
			prj.fecha_recepcion = datetime.fromisoformat(proyecto.get('create_date').replace('Z', '')) if proyecto.get('create_date') != '0000-00-00' else None 
			prj.fecha_estimada_conexion = datetime.fromisoformat(proyecto.get('fecha_estimada_conexion').replace('Z', '')) if proyecto.get('fecha_estimada_conexion') != '0000-00-00' else None
			prj.capacidad = proyecto.get('potencia_nominal', '')
			dbh.session.commit()
			
			if prj.representantes.count() <= 0 :
				files = process.get_record_files(proyecto)
				people_data = None
				for _file_ in files:
					if 'formulario' not in _file_.get('nombre').lower():
						continue
					people_data = process.find_file_data(_file_)
					if people_data is not None:
						break
				
				if people_data is not None:
					print(people_data[0])
					dbh.session.add_all( [ RepresentanteLegal(**people, proyecto_id=prj.id) for people in people_data[0] ] )
					dbh.session.add_all( [ Coordinador(**people, proyecto_id=prj.id) for people in people_data[1] ] )
					dbh.session.commit()
					
		
		else: 
			prj = Project()
			prj.external_id = external_id
			prj.proyecto_id = proyecto.get('proyecto_id')
			prj.nombre = proyecto.get('proyecto')
			prj.tecnologia = proyecto.get('tipo_tecnologia_nombre')
			prj.empresa = proyecto.get('empresa_solicitante', '')
			if prj.empresa == 'undefined':
				prj.empresa = proyecto.get('razon_social', '')
			prj.tipo = proyecto.get('tipo_solicitud')
			prj.estado = proyecto.get('provincia')
			prj.region = proyecto.get('region')
			prj.comuna = proyecto.get('comuna')
			prj.estado_solicitud = proyecto.get('estado_solicitud')
			_create_date = proyecto.get('create_date')
			_fecha_estimada_conexion = proyecto.get('fecha_estimada_conexion', '')
			prj.fecha_recepcion = datetime.fromisoformat(_create_date.replace('Z', '')) if _create_date is not None and _create_date != '0000-00-00' else None 
			prj.fecha_estimada_conexion = datetime.fromisoformat(_fecha_estimada_conexion.replace('Z', '')) if _fecha_estimada_conexion is not None and _fecha_estimada_conexion != '0000-00-00' else None
			prj.capacidad = proyecto.get('potencia_nominal', '')
			
			files = process.get_record_files(proyecto)
			people_data = None
			for _file_ in files:
				if 'formulario' not in _file_.get('nombre').lower():
					continue
				people_data = process.find_file_data(_file_)
				if people_data is not None:
					break
			
			if people_data is not None:
				print(people_data[0])
				prj.representantes = [ RepresentanteLegal(**people) for people in people_data[0] ]
				prj.coordinadores = [ Coordinador(**people) for people in people_data[1] ]
			
			dbh.session.add(prj)
			dbh.session.commit()
	
	return redirect( url_for('panel.proyectos') )
