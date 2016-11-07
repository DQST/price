from django.shortcuts import redirect
from django.views.generic import View
from django.conf import settings
from main_site.models import *
from .form import *


class ParseView(View):
	def load(self, obj, file, category, dealer):
		import xml.etree.ElementTree as ET

		file = file[::-1]
		file = file.replace(file[:file.find('.')], 'lmx')
		file = file[::-1]
		path = '%s/%s' % (settings.MEDIA_ROOT, file)
		tree = ET.parse(path)
		root = tree.getroot()

		category = Categories.objects.get(pk=category)

		object_root = root.find('objects')
		for o in object_root.findall('object'):
			p = Products()
			p.category = category
			p.dealer = dealer
			for k in obj.keys():
				for i in o.findall('field'):
					if obj[k] == i.get('name'):
						p.__dict__[k] = i.text
			p.save()


	def post(self, request):
		import json
		parse_form = ParseForm(request.POST)
		if parse_form.is_valid():
			json_str = parse_form.cleaned_data.get('connections')
			file = parse_form.cleaned_data.get('file')
			category = parse_form.cleaned_data.get('category')
			dealer = parse_form.cleaned_data.get('dealer')
			
			if not Dealer.objects.filter(name=dealer).exists():
				Dealer.objects.create(name=dealer)
			dealer = Dealer.objects.get(name=dealer)
			
			json_object = json.loads(json_str)
			self.load(json_object, file, category, dealer)
		return redirect('/price/')
