from django.test import TestCase, Client
from .models import *
from .views import *


class ViewsTest(TestCase):
	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)

	def test_upload_file(self):
		response = self.client.post('/login/', {'login':'admin', 'password':'qwert123'}, follow=True)
		self.assertEqual(response.status_code, 302)
		with open('D:/МАмалыш РРЦ NOORDI от 05.07.2016.xls', 'rb') as fp:
			response  = self.client.post('/price/upload/', {'q':2, 'file': fp, 'row_head_offset': 1, 'row_data_offset': 2})
		self.assertEqual(response.status_code, 200)


class ModelsTest(TestCase):
	def setUp(self):
		Documents.objects.create(docfile='test_file.xls')

	def test_document(self):
		docs = Documents.objects.all()
		self.assertEqual(len(docs), 1)
