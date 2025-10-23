from flask import current_app, g, url_for
import json

from flaskr.common.functions import *

def register(app):

	@app.template_filter()
	def json_decode(_str_):
		if _str_ is None or not _str_:
			return None

		print('JSON FILTER:', _str_)
		return json.loads(_str_)

	@app.template_filter()
	def asset_url(filename):
		
		# return url_for('static', filename=get_asset_path(filename, is_admin=is_admin()))
		return url_for('static', filename=get_asset_path(filename, is_admin=False))
