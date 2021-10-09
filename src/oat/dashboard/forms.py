from django import forms
from .models import Category, Menu


class CategoryModelForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('published','created_on','updated_on')

class MenuModelForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('published','created_on','updated_on')
