# -*- coding: utf-8 -*-
import pandas as pd
import openpyxl

class XlsReader:

	def __init__(self):
		self.filename = None
		self.wb = None
		self.sheet = None
		self.rows = []
		
	def read(self):
		
		# data = pd.ExcelFile(self.filename)
		data = pd.read_excel(self.filename, sheet_name='FORMULARIO SAC')
		print(data.to_dict('records'))
		# print(data.iloc[8])
		# print(data.iloc[8,0])
		# print(data.loc[9])
		# print(data.iloc[9,5])
		# print(data.loc[10])
	
	def read_pyxl(self):
		self.wb = openpyxl.load_workbook(self.filename)
		# print('sheets', self.wb.worksheets, self.wb.active)
		
		for sheet in self.wb.worksheets:
			for row in sheet.rows:
				for cell in row:
					if type(cell.value) == str and 'Contacto de Representante Legal' in cell.value:
						print(cell.value)
						self.sheet = sheet
						break
						
		if self.sheet is None:
			return False
			
		# for row in self.wb.active.rows:
		for row in self.sheet.rows:
			row_data = []
			# print(row)
			for cell in row:
				row_data.append(cell.value)
				
			# print(row_data)
			self.rows.append(row_data)
			
	def get_rep_legal(self):
		items = []
		for i in range(len(self.rows)):
			row = self.rows[i]
			
			# print(row)
			if row[1] is not None and 'Nombre del Representante Legal' in row[1]:
				data = {
					'nombre': row[5],
					'email': self.rows[i + 1][3],
					'telefono': self.rows[i + 1][9]
				}
				items.append(data)
		
		return items
		
	def get_coordinadores(self):
		items = []
		for i in range(len(self.rows)):
			row = self.rows[i]
			
			# print(row)
			if row[1] is not None and 'Nombre coordinador de proyecto' in row[1]:
				data = {
					'nombre': row[5],
					'email': self.rows[i + 1][3],
					'telefono': self.rows[i + 1][9]
				}
				items.append(data)
		
		return items
		
if __name__ == '__main__':
	xls = XlsReader()
	xls.filename = '/Volumes/HDD2/temp/27-08-2024_Formulario-de-solicitud-y-antecedentes-SAC.xlsx'
	xls.read_pyxl()
	reps = xls.get_rep_legal()
	coords = xls.get_coordinadores()
	
	print(reps, coords)

