from django.shortcuts import redirect
from main_site.models import *


class ParseView(View):
	def load(self, obj, file, category, dealer):
		import xml.etree.ElementTree as ET

		file = file[:file.index('.')+1]+'xml'
		path = '%s/uploads/%s' % (settings.MEDIA_ROOT, file)
		tree = ET.parse(path)
		root = tree.getroot()

		category = Categories.objects.get(pk=category)

		object_root = root.find('objects')
		for o in object_root.findall('object'):
			p = Products()
			p.category = category
			p.dealer = dealer
			for key in obj.keys():
				p.__dict__[key] = o.find(obj[key]).text
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
