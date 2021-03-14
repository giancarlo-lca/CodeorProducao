from django import forms

from .models import Csv, Xls

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('arquivo',)

class XlsxModelForm(forms.ModelForm):
    class Meta:
        model = Xls
        fields = ('arquivo',)