import openpyxl
import xml.etree.ElementTree as ET
import yattag


class ConvertToXML:
	def __init__(self, path, head_row=0, start_row=1):
		wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
		self.sh = wb.active
		self.headers = [i.value.capitalize() for i in self.sh[head_row:head_row] if i.value is not None]
		for i in range(len(self.headers)):
			self.headers[i] = self.headers[i].strip()
			self.headers[i] = self.headers[i].replace(' ', '_')
			self.headers[i] = self.headers[i].replace('\n', '')
		self.start_row = abs(start_row) - 1
		self.objects = self.__parse(head_row)
	
	def __is_empty(self, obj):
		none_count = 0
		for i in obj:
			if i[1] is None:
				none_count += 1
		if none_count != len(obj):
			return False
		return True
	
	def __parse(self, head_row):
		out = []
		for row in self.sh.iter_rows(row_offset=self.start_row):
			obj = [(key, el.value) for key, el in zip(self.headers, row)]
			out.append(obj)
		return out
	
	def save(self, path):
		'''Doc string:
		Save file as xml using argument: path'''
		root = ET.Element('root')
		tree = ET.ElementTree(root)
		
		'''create headers element'''
		headers = ET.SubElement(root, 'headers')
		headers.set('count', str(len(self.headers)))
		length = len(self.headers) + 1
		for n, key in zip(range(1, length), self.headers):
			el = ET.SubElement(headers, 'head')
			el.text = key.capitalize()
			el.set('id', str(n))
		
		'''create objects element'''
		objects = ET.SubElement(root, 'objects')
		objects.set('count', str(len(self.objects)))
		length = len(self.objects) + 1
		for n, obj in zip(range(1, length), self.objects):
			if self.__is_empty(obj):
				continue
			o = ET.SubElement(objects, 'object')
			o.set('id', str(n))
			for j in obj:
				ET.SubElement(o, j[0]).text = str(j[1])
		
		'''save into the file'''
		xmlstr = ET.tostring(root, encoding='utf-8', short_empty_elements=False)
		xmlstr = xmlstr.decode('utf-8').replace('None', '')
		pretty_xml_string = yattag.indent(
			xmlstr,
			indentation = '\t',
			newline = '\r\n'
		)
		with open(path, 'wb') as f:
			f.write('<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8'))
			f.write(pretty_xml_string.encode('utf-8'))
