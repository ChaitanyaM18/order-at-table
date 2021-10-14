from django import forms
from django.db.models import fields
from .models import UserDetails,GetUserReview


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = UserDetails
        exclude = ('user_table_no','published','created_on','updated_on','user_email','address')

class UserReviewForm(forms.ModelForm):

    class Meta:
        model = GetUserReview
        fields = "__all__"