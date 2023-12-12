from django import forms

class ImportarCensoForm(forms.Form):
    archivo = forms.FileField()