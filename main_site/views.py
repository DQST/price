from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from .form import *
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SearchView(View):
	def parse(self, query, filter_by):
		if filter_by == 'articul':
			data = Products.objects.filter(articul=query)
		else:
			data = Products.objects.filter(name__icontains=query)
		return data

	def get_pagintations(self, paginator=None, articles=None, cur_page=0, max_pages_count=9):
		if paginator is None and articles is None:
			return None

		paginations = [i+1 for i in range(paginator.num_pages)]
		if paginator.num_pages > max_pages_count:
			if len(articles) == 1:
				articles = articles[0]
			if 0 <= cur_page < 7:
				paginations = paginations[:9]
				paginations.extend(['...', paginator.num_pages])
			elif paginator.num_pages - 7 <= cur_page <= paginator.num_pages:
				paginations = paginations[-9:]
				paginations.reverse()
				paginations.extend(['...', 1])
				paginations.reverse()
			elif 7 <= cur_page <= paginator.num_pages - 5:
				paginations = paginations[cur_page-4:cur_page+5]
				paginations.extend(['...', paginator.num_pages])
				paginations.reverse()
				paginations.extend(['...', 1])
				paginations.reverse()
		return paginations
	
	def get(self, request):
		if not request.user.is_authenticated():
			return redirect('/')
		return render(request, 'main_site/rezult.html')


class AjaxView(SearchView):
	def get(self, request):
		form = SearchForm(request.GET)
		if form.is_valid():
			q = form.cleaned_data.get('query')
			filter_by = form.cleaned_data.get('search_filter')
			page = int(form.cleaned_data.get('p'))
			data = self.parse(q, filter_by)
			paginator = Paginator(data, per_page=30, orphans=10)

			try:
				articles = paginator.page(page)
			except PageNotAnInteger:
				articles = paginator.page(1)
			except EmptyPage:
				articles = paginator.page(paginator.num_pages)
			
			paginations = self.get_pagintations(paginator=paginator, articles=articles, cur_page=page)
			
			return render(request, 'main_site/table.html', {'query': q, 'articles': articles, \
				'p': page, 'paginations': paginations})
		return redirect('/price/')


class FastSearchView(SearchView):
	def get(self, request):
		from django.http import HttpResponse
		if 'q' in request.GET and request.GET['q']:
			q = request.GET['q']
			data = self.parse(q, 'name')
			if data:	
				return HttpResponse('$'.join([i.name for i in data]))
		return HttpResponse('Ничего не найдено: %s' % q)


class ImportView(View):
	def get_info(self, s):
		import re
		file = ''
		for i in reversed(s):
			if i != '/':
				file += i
				continue
			break
		comp = re.compile('^\w+\.')
		f_ext = comp.match(file).group(0)
		f_name = ''.join(file.replace(f_ext, ''))
		return f_name[::-1], f_ext[::-1][1:]

	def post(self, request):
		from .convert import ToXML, ConXLS
		import transliterate
		from transliterate import slugify, detect_language

		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			file = form.cleaned_data.get('file')
			head_offset = form.cleaned_data.get('row_head_offset')
			data_offset = form.cleaned_data.get('row_data_offset')
			
			name, ext = self.get_info(file.name)
			
			if detect_language(name):
				name = slugify(name)

			file.name = '%s.%s' % (name, ext)
			newdoc = Documents(docfile=file)
			newdoc.save()
			
			path = '%s%s' % (settings.MEDIA_ROOT, newdoc.docfile.name)
			
			if ext == 'xls':
				xls_file = ConXLS(path)
				path = path.replace('xls', 'xlsx')
				xls_file.save(path)
			
			xml = ToXML(path, head_offset, data_offset)
			xml.save(path.replace('xlsx', 'xml'))
			
			headers = ','.join(xml.headers)
			return redirect('/price/upload/?q=2&fn={name}&f_size={size}&headers={headers}'.format(name=name+'.'+ext, \
				size=file.size, headers=headers))
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
