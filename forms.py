from django import forms
from .models import *
from django.forms import ImageField, ModelForm, NumberInput, TextInput

# class CategoryForm(ModelForm):
#   class Meta:
#     model = ProductCategory
#     fields = ["name"]
#     widgets = {
#       "name":TextInput(attrs={
#       'placeholder':'Category name',
#       }),
#   }

# class SellItemForm(ModelForm):
#   class Meta:
#     model = SellItems
#     fields = ["title","price","description"]
#     widgets = {
#       "title":TextInput(attrs={
#       'placeholder':'Item name',
#       }),
#       "price":NumberInput(attrs={
#       'placeholder':'Item price',
#       }),
#       "description":TextInput(attrs={
#       'type':'Item description'
#       }),
#   }


class CategoryForm(forms.Form):
  name = forms.CharField(required=True, label=(u'Name'))

class SellItemForm(CategoryForm):
  title = forms.CharField(required=True,max_length=100)
  price = forms.FloatField(required=True)
  description = forms.CharField(required=True)
  image = forms.ImageField(required=False)

  