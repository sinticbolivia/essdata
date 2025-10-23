# -*- coding: utf-8 -*-
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)
from flaskr.common.functions import *
from flaskr.factory import Factory
from datetime import datetime
from sqlalchemy import and_, or_, not_
import json

bp = Blueprint('common', __name__)


@bp.route('/js/config')
def js_config():
	config = {
		'app_ame': '',
		'baseurl': request.url.replace('/js/config', ''), # request.base_url,
	}
	js = 'const AppConfig = {0};'.format( json.dumps(config) )
	
	response = make_response(js, 200)
	response.mimetype = 'text/javascript'
	return response
