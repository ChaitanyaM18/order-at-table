from django import forms
from .models import UserDetails


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = UserDetails
        exclude = ('user_table_no','published','created_on','updated_on')
