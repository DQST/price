from django import forms


class ParseForm(forms.Form):
	connections = forms.CharField()
	file = forms.CharField()
	category = forms.IntegerField()
	dealer = forms.CharField(max_length=255)
