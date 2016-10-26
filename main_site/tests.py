from django.test import TestCase, Client
from .models import *


class ModelsTest(TestCase):
	def setUp(self):
		Documents.objects.create(docfile='test_file.xls')
		Products.objects.create(articul=631, name='NOORDI Коляска 3 в 1 SUN SPORT (автокресло+короб+прогулка,кожаная ручка) Молочный, шт.')

	def test_document(self):
		docs = Documents.objects.all()
		self.assertEqual(len(docs), 1)

	def test_articul(self):
		o =  Products.objects.filter(articul=631)
		self.assertEqual(len(o), 1)
