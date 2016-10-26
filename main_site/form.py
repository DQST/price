from django import forms


class SearchForm(forms.Form):
	query = forms.CharField()
	search_filter = forms.CharField()
	p = forms.IntegerField()


class LoginForm(forms.Form):
	login = forms.CharField()
	password  = forms.CharField(min_length=8, max_length=16)


class DocumentForm(forms.Form):
	file = forms.FileField()
	row_head_offset = forms.IntegerField()
	row_data_offset = forms.IntegerField()


class ParseForm(forms.Form):
	connections = forms.CharField()
	file = forms.CharField()
	category = forms.IntegerField()
	dealer = forms.CharField(max_length=255)


class ImportForm(forms.Form):
	q = forms.IntegerField()
	fn = forms.CharField()
	f_size = forms.FloatField()
	headers = forms.CharField()
