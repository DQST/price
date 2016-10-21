from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from .form import *
from .convert import ToXml
from django.conf import settings


class SearchView(View):
	def check(self, data):
		multiple = False
		if len(data) == 1:
			data = data[0]
		elif len(data) > 1:
			multiple = True
		return data, multiple

	def parse(self, query, filter_by):
		if filter_by == 'articul':
			data = Products.objects.filter(articul=query)
		else:
			data = Products.objects.filter(name__contains=query)
		return self.check(data)

	def get(self, request):
		multiple, data_len, pages, p = False, None, None, 0
		if not request.user.is_authenticated():
			return redirect('/')
		
		form = SearchForm(request.GET)
		if form.is_valid():
			q = form.cleaned_data.get('query')
			filter_by = form.cleaned_data.get('search_filter')
			if 'p' in request.GET and request.GET['p']:
				p = int(request.GET['p'])
			page_offset = p * 30
			data, multiple = self.parse(q, filter_by)
			
			if multiple:
				data_len = len(data)
				pages = [i+1 for i in range(round(data_len / 30))]
				data = data[page_offset : 30 + page_offset]
			
			return render(request, 'main_site/rezult.html', {'query': q, 'data': data, 'data_len': data_len , \
				'multiple': multiple, 'user': request.user, 'pages': pages, 'p': p})
		return render(request, 'main_site/rezult.html', {'user': request.user})


class ImportView(View):
	def post(self, request):
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			file = form.cleaned_data.get('file')
			head_offset = form.cleaned_data.get('row_head_offset')
			data_offset = form.cleaned_data.get('row_data_offset')
			newdoc = Documents(docfile=file)
			newdoc.save()
			conv = ToXml('%s/uploads/%s' % (settings.MEDIA_ROOT, file.name), head_offset, data_offset)
			conv.save('%s/uploads/%s.xml' % (settings.MEDIA_ROOT, file.name[:file.name.index('.')]))
			headers = ','.join(conv.headers)
			return redirect('/price/upload/?q=2&fn=%s&f_size=%s&headers=%s' % (file.name, file.size, headers))
		return render(request, 'main_site/import.html', {'errors': form.errors})

	def get(self, request):
		if not request.user.is_authenticated():
			return redirect('/')
		form = ImportForm(request.GET)
		if form.is_valid() and form.cleaned_data.get('q') == 2:
			categories_list = Categories.objects.all()
			file_name = form.cleaned_data.get('fn')
			file_size = form.cleaned_data.get('f_size')
			headers = form.cleaned_data.get('headers')
			return render(request, 'main_site/import2.html', {
				'categories_list': categories_list,
				'file_name': file_name,
				'file_size': file_size,
				'headers': headers.split(','),
			})
		return render(request, 'main_site/import.html')


class ParseView(View):
	def load(self, obj, file, category, dealer):
		import xml.etree.ElementTree as ET
		file = file[:file.index('.')] + '.xml'
		tree = ET.parse('%s/uploads/%s' % (settings.MEDIA_ROOT, file))
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
