from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.files import File
from .models import SCategories, Document
from .form import SearchForm, DocumentForm, ImportForm
from .convert import ConvertToXML
from django.conf import settings


class SearchView(View):
	def get(self, request):
		if not request.user.is_authenticated():
			return redirect('/')
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data.get('query')
			data = None
			return render(request, 'main_site/rezult.html', {'query': query, 'data': data})
		return render(request, 'main_site/rezult.html')


class ImportView(View):
	def post(self, request):
		if not request.user.is_authenticated():
			return redirect('/')
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			file = form.cleaned_data.get('file')
			head_offset = form.cleaned_data.get('row_head_offset')
			data_offset = form.cleaned_data.get('row_data_offset')
			newdoc = Document(docfile=file)
			newdoc.save()
			conv = ConvertToXML('%s/uploads/%s' % (settings.MEDIA_ROOT, file.name), head_offset, data_offset)
			conv.save('%s/uploads/%s.xml' % (settings.MEDIA_ROOT, file.name[:file.name.index('.')]))
			headers = ','.join(conv.headers)
			return redirect('/price/upload/?q=2&fn=%s&f_size=%s&headers=%s' % (file.name, file.size, headers))
		return render(request, 'main_site/import.html', {'errors': form.errors})

	def get(self, request):
		if not request.user.is_authenticated():
			return redirect('/')
		form = ImportForm(request.GET)
		if form.is_valid() and form.cleaned_data.get('q') == 2:
			categories_list = SCategories.objects.all()
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
	def post(self, request):
		if not request.user.is_authenticated():
			return redirect('/')
