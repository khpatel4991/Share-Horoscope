from django import forms
from .models import Stock

class AddShareForm(forms.ModelForm):
    class Meta:
        model = Stock