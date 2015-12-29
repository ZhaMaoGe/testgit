from django import forms


class WebForm(forms.Form):
	webfile = forms.FileField()
