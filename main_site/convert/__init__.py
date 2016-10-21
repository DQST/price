import openpyxl
from yattag import *
import codecs

class BConverter(object):
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
	
	def __parse(self, head_row):
		out = []
		for row in self.sh.iter_rows(row_offset=self.start_row):
			obj = [(key, (lambda x: '' if x is None else x)(el.value)) for key, el in zip(self.headers, row)]
			out.append(obj)
		return out
	
	def save(self, path):
		raise Exception('Переопределить метод!')

class ToXml(BConverter):
	def save(self, path):
		'''Doc string:
		Save file as xml using argument: path'''
		doc, tag, text, line = Doc().ttl()

		headers_len = len(self.headers)
		objects_len = len(self.objects)
		doc.asis('<?xml version="1.0" encoding="utf-8"?>')
		with tag('root'):
			with tag('headers', count=headers_len):
				for i, key in zip(range(1, headers_len + 1), self.headers):
					line('head', key, id=str(i))
			with tag('objects', count=objects_len):
				for i, obj in zip(range(1, objects_len + 1), self.objects):
					with tag('object', id=str(i)):
						for key, value in obj:
							with tag(key):
								text(value)

		pretty_string = indent(
			doc.getvalue(),
			indentation = '\t',
			newline = '\n',
		)

		with codecs.open(path, 'w', encoding='utf-8') as f:
			f.write('%s\n' % pretty_string)
