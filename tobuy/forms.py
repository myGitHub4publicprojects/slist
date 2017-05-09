from django import forms
from .models import List

class ListForm(forms.ModelForm):
    name = forms.CharField(max_length=120, label='New list name')
    class Meta:
        model = List
        fields = ['name']

class InviteForm(forms.Form):
    email = forms.EmailField()