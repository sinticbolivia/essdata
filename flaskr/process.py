import os
import requests
# from html.parser import HTMLParser
from lxml import etree

def search_string(text: str, keyword: str):
	return True if keyword in text else False

def search_strings(text: str, keywords: list):
	found = False
	for keyword in keywords:
		found = keyword in text
		if found:
			break

	return found

	
def get_json():
	url = 'https://pkb3ax2pkg.execute-api.us-east-2.amazonaws.com/prod/data/public?tipo=6&anio=2024&tipo_solicitud_id=0&solicitud_id=null'
	res = requests.get(url)
	records = res.json()

	return records

def get_matches(data: list):
	keywords = ['BESS', 'Almacenamiento', 'SAE']
	matches = []

	for record in data:
		# print(record.get('proyecto'))

		if search_strings(record.get('proyecto', ''), keywords) is False:
			continue

		print(record.get('proyecto'))
		matches.append(record)

	return matches

def get_record_files(record: dict):
	print(record.get('proyecto'))
	url = 'https://pkb3ax2pkg.execute-api.us-east-2.amazonaws.com/prod/data/public?tipo=11&anio=null&tipo_solicitud_id=null&solicitud_id={0}'.format(record.get('id'))
	print(url)
	res = requests.get(url)
	items = res.json()
	
	return items
	'''
	files = []
	for item in items:
		# print(item)
		
		if 'sac' in item.get('nombre', '').lower():
			files.append(item)
		
		# file_url = get_file_url(item.get('ruta_s3'), item.get('nombre'))
		#print(file_url)
	
	return files
	'''

def get_file_url(path: str, filename: str):
	url = 'https://pkb3ax2pkg.execute-api.us-east-2.amazonaws.com/prod/documentos/s3?key={0}&download={1}'.format(path, filename)
	res = requests.get(url)
	
	data = res.json()
	
	return data;
	
def get_file_buffer(path: str, filename: str):
	data = get_file_url(path, filename)
	print(data.get('url_archivo'))
	res = requests.get(data.get('url_archivo'))
	
	return res.content

def find_pdf_data(_buffer_, is_file=False):
	from .pdf_reader import PdfReader, PyPdfReader
	reader = PyPdfReader()
	reader.extract(_buffer_)
	reps = reader.get_rep_legal()
	coords = reader.get_coordinadores()
	# print(reps, coords)
	if len(reps) <= 0 or len(coords) <= 0:
		return None
		
	return (reps, coords)

def find_xlsx_data(filename):
	from .xlsx_reader import XlsReader
	
	xls = XlsReader()
	xls.filename = filename
	xls.read_pyxl()
	reps = xls.get_rep_legal()
	coords = xls.get_coordinadores()
	
	if len(reps) <= 0 or len(coords) <= 0:
		return None
		
	return (reps, coords)
	
def find_file_data(_file_):
	print(_file_)
	_buffer_ = get_file_buffer(_file_.get('ruta_s3'), _file_.get('nombre'))
	
	if '.xlsx' in _file_.get('nombre'):
		with open(_file_.get('nombre'), 'wb') as file:
			file.write(_buffer_)
			file.close()
		data = find_xlsx_data(_file_.get('nombre'))
		os.remove(_file_.get('nombre'))
		return data
		
	elif '.pdf' in _file_.get('nombre'):
		'''
		with open(_file_.get('nombre'), 'wb') as file:
			file.write(_buffer_)
			file.close()
		'''
		# find_pdf_data(_file_.get('nombre'), True)
		return find_pdf_data(_buffer_)
		
		
	return None
	
def cruzar_data(keyword: str):
	post = {
		'seia_project_name': "BESS+Chaguales",
		'seia_region':		"",
		'seia_sector':		"",
		'op':	"Buscar",
		'form_build_id':	"form-vSq19hFN5HaDVkZ7sTazEumY_Z9nL-KkqBIUZxtKYGg",
		'form_id':			"sea_core_seia_project_search_form",
	}
	url = f'https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php?nombre={keyword}'
	print('CRUZAR DATA', f'"{url}"')
	res = requests.get(url)
	print(res.text)
	parser = etree.HTMLParser() # fromstring(res.text)
	root = etree.fromstring(res.text, parser)
	tables = root.xpath('//table')
	print('tables', tables)
	
if __name__ == '__main__':
	data = get_json()
	matches = get_matches(data)
	print('Matches: ', len(matches))
	# print(matches)
	# '''
	for record in matches:
		files = get_record_files(record)
		record['files'] = files
		# print(files)
		people_data = None
		for _file_ in files:
			if 'formulario' not in _file_.get('nombre').lower():
				continue
			people_data = find_file_data(_file_)
			if people_data is not None:
				break
				
		record['people_data'] = {
			'reps': people_data[0],
			'coords': people_data[1]
		}
		
		print(record)
		
		quit()
		# cruzar_data(record.get('proyecto'))

	# print(matches)
	# '''
	


