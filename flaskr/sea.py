import os
import requests
from lxml import etree
import pandas as pd
import numpy as np
import time

_filename = 'sea.csv'

def obtener_fecha(id):
	url = 'https://seia.sea.gob.cl/expediente/newPlazos.php?modo=ficha&id_expediente={0}'.format(id)
	res = requests.get(url)
	parser = etree.HTMLParser() 
	root = etree.fromstring(res.text, parser)
	row = root.find('.//table[@class="tabla_uso_tiempo"]//tr[@class="bar-simple"]')
	# print('row time data', etree.tostring(row))
	
	return row.findall('td')[2].text
	
def get_page_items(page_table):
	items = []
	rows = page_table.xpath('//tbody/tr')
	for row in rows:
		cells = row.findall('td')
		link = cells[1].find('a')
		id = link.get('href').split('id_expediente=')[1]
		fecha = obtener_fecha(id)
		
		data = {
			'id': id,
			'nombre': link.text,
			#'link': link.get('href'),
			'estado': cells[9].text,
			'fecha_plazo_evaluacion': fecha
		}
		# print(data)
		items.append(data)
		
	return items
	
def search(keyword: str):
	url = 'https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php?nombre={0}&sector=7'.format(keyword)
	res = requests.get(url)
	# print('COOKIES', res.cookies)
	parser = etree.HTMLParser() 
	root = etree.fromstring(res.text, parser)
	pages = root.xpath('//select[@name="pagina_offset"]');
	print('pages', pages)
	if len(pages) <= 0:
		return None
	pages = pages[0].xpath('//option')
	total_pages = len(pages)
	tables = root.xpath('//table')
	# print('tables', tables)
	items = get_page_items(tables[0])
	
	for page in range(2, total_pages + 1):
		page_url = '{0}&_paginador_refresh=1&_paginador_fila_actual={1}'.format(url, page)
		print('page_url', page_url)
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
			'Host': 'seia.sea.gob.cl',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0',
			'Upgrade-Insecure-Requests': 1,
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Site': 'cross-site',
			'Pragma': 'no-cache',
			'Priority': 'u=0, i',
		}
		page_res = requests.get(page_url, cookies=res.cookies, allow_redirects=True)
		# print(page_res.text)
		page_root = etree.fromstring(page_res.text, parser)
		page_table = page_root.find('.//table[@class="tabla_datos"]')
		if page_table is None:
			print(f'page {page}: table data not found')
			continue
		
		page_items = get_page_items(page_table)
		items.extend( page_items )
		
	# print(items)
	# print('total items: ', len(items))
	return items

def search_keywords():
	items = []
	if os.path.isfile(_filename):
		print("last modified: %s" % time.ctime(os.path.getmtime(_filename)))
		return pd.read_csv(_filename)
	
	for keyword in ['bess', 'almacenamiento de energia']:
		kitems = search(keyword)
		items.extend(kitems)
		
	print('global total items: ', len(items))
	df = pd.DataFrame(items)
	df.to_csv(_filename, index=False)
	
	return df
	#return pd.read_csv(_filename)
	
if __name__ == '__main__':
	df = search_keywords()
	
	print(df)
	# matches = df[df['nombre'] == 'San Rafael']
	matches = df[df['nombre'].str.contains('Cachapoal')]
	if matches.size <= 0 :
		print('No matches found')
		quit()
		
	print(matches)
	print(matches.iloc[0]['nombre'], ' -> ', matches.iloc[0]['fecha_plazo_evaluacion'])
	# print(matches.to_dict())
