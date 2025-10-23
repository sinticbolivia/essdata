# -*- coding: utf-8 -*-
import os,sys,inspect
import io
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# print(parentdir)
# sys.path.insert(0, currentdir + '/libs')
import time
# import PyPDF2
import pypdf
import json
from pdfquery import PDFQuery
import re

class PyPdfReader:
	
	def __init__(self):
		self.reader = None
		self.text = None
		self.pages = []
	
	def extract_from_file(self, filename):
		fh = open(filename, 'rb')
		_buffer_ = fh.read()
		fh.close()
		self.extract(_buffer_)
		
	def extract(self, _buffer_):
		self.reader = pypdf.PdfReader(io.BytesIO(_buffer_))
		print('pages', self.reader.pages)
		for page in range(len(self.reader.pages)):
			pageObj = self.reader.pages[page]
			text_page = pageObj.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
			self.pages.append(text_page)
			# self.pages.append(re.sub(r'\s{1}(?=\w)', '', text_page))
			# print(text_page)
			# print(re.sub(r'(?<=\w)\s{1}(?=\w)', '', text_page))
			# print(re.sub(r'\s{1}(?=\w)', '', text_page))
			# print(re.sub(r'(?<=^|\b\w) +(?=\w\b|$)', '', text_page))
			# print(re.sub(r'([a-zA-Z])\s{1}([a-zA-Z])', '$1$2', text_page))
			
		#print([page for page in self.pages])
		
	def extract_people_data(self, line: str, data_line: str):
		print(line)
		print(data_line)
		# name_data = re.findall(r'([a-zA-Záéíóú\s]+)', line.strip())
		# data_data = re.findall(r'([a-zA-Záéíóú\s{1}\-\.@]+)\s+', data_line.strip())
		name_data = re.sub(r'\s{2,}', '::', line.strip()).split('::')
		contact_data = re.sub(r'\s{2,}', '::', data_line.strip()).split('::')
		# print(name_data, data_data)
		# print(data_data)
		# quit()
		if len(name_data) < 2:
			return None
			
		data = {
			'nombre': name_data[1].strip(),
			'email': contact_data[1] if len(contact_data) >= 2 else '',
			'telefono': contact_data[3] if len(contact_data) >= 4 else '',
		}
		return data
		
	def get_rep_legal(self):
		items = []
		
		for page in self.pages:
			lines = page.splitlines()
			for line_i in range(len(lines)):
				line = lines[line_i]
				if 'Nombre del Representante Legal' in line or 'Nombredel  RepresentanteLegal' in line:
					data_line = lines[line_i + 1]
					data = self.extract_people_data(line, data_line)
					if data is None:
						continue
					items.append(data)
					
		# print(items)
		return items
		
	def get_coordinadores(self):
		items = []
		
		for page in self.pages:
			lines = page.splitlines()
			for line_i in range(len(lines)):
				line = lines[line_i]
				if 'Nombre coordinador de proyecto' in line:
					data_line = lines[line_i + 1]
					data = self.extract_people_data(line, data_line)
					if data is None:
						continue
					
					items.append(data)
		
		# print(items)
		
		return items
	
class PdfReader:
	detail_start_index = -1
	detail_end_index = -1
	_MAX_TRIES_ = 10
	_TEMP_DIR_ = currentdir + '/temp'

	def __init__(self):
		self.get_next = None
		self.reader = None
		self.fh = None
		self.pages = 0
		self.lines = []
		self.filename = None
		
	def set_buffer(self, _buffer_):
		self.reader = PyPDF2.PdfReader(io.BytesIO(_buffer_))
	
	def set_file(self, filename):
		#self.fh = open(pdf_file, 'rb')
		#self.reader = PyPDF2.PdfReader(self.fh)
		print('file: ', filename)
		self.filename = filename
		self.reader = PDFQuery(filename)
		self.reader.load()
		
	def start(self):
		# pass
		# self._get_data()
		self.reader.tree.write(self.filename + '.xml', pretty_print=True)
		
	def close(self):
		self.reader = None
		if self.fh:
			self.fh.close()
			
	def _get_data(self):
		self.pages = len(self.reader.pages)
		
	def find_text(self, keyword: str):
		label = self.reader.pq('LTTextLineHorizontal:contains("{0}")'.format(keyword))
		print('FIND RESULT', label)
		return True if label else False
		
		'''
		self.parse_pdf()
		i = 0
		for line in self.lines:
			print('LINE:', i, line)
			i += 1
		'''
		
	def parse_pdf(self):
		
		def _func_visitor_body_(text, cm, tm, fontDict, fontSize):
			# print(cm)
			# print(tm)
			if not text.strip() or text == '\n':
				return
			text = text.strip().strip('\n')
			
			self.lines.append(text)
		
		for page in range(len(self.reader.pages)):
			pageObj = self.reader.pages[page]
			# print('Page: {0}'.format(page))
			# print(pageObj)
			pageObj.extract_text(visitor_text=_func_visitor_body_)
			
		# print(self.lines)
		'''
		for index in range(len(lines)):
			line = lines[index]
			if not line:
				continue
		'''
		
	def get_rep_legal(self):
		data = {
			'nombre': self.reader.pq('LTTextLineHorizontal:in_bbox("212.681, 220.745, 290.297, 231.724")').text(),
			'email': self.reader.pq('LTTextLineHorizontal:in_bbox("251.714, 698.425, 346.938, 709.425")').text()
		}
		return data

if __name__ == '__main__':
	pdf = PyPdfReader()
	# pdf.extract_from_file('/Users/marcelo/Downloads/Formulario-de-solicitud-y-antecedentes-SAC-1-1.pdf')
	pdf.extract_from_file('/Users/marcelo/Downloads/Formulario-Proyecto-Fehaciente_BESS_Santa_Lya_160_MW.pdf')
	coords = pdf.get_coordinadores()
	reps = pdf.get_rep_legal()
	print(reps, coords)
