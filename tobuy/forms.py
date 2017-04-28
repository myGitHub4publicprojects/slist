from django import forms
from .models import Item, List

class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=120, label='')
    class Meta:
        model = Item
        fields = ['name']

class ListForm(forms.ModelForm):
    name = forms.CharField(max_length=120)
    class Meta:
        model = List
        fields = ['name']

class InviteForm(forms.Form):
    email = forms.EmailField()