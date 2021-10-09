from django import forms
from django.conf import settings
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm




class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username','password','groups','email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("user with this name already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken!")
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        print("user pass", user.password)
        user.set_password(user.password)
        # do custom stuff
        if commit:
            user.save()
        return user



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','groups','email')

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        print("user pass", user.password)
        user.set_password(user.password)
        # do custom stuff
        if commit:
            user.save()
        return user



class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')



class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.status == "Active" or user.groups.status == "Inactive":
            raise forms.ValidationError(
                'Your account is inactive', code='invalid_login')



class ProfileUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('photo',)
