from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib import admin
from django.contrib.auth.models import Permission
from . import models

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('username','status','email','groups')  # Contain only fields in your `custom-user-model'
    filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions
    UserAdmin.fieldsets += ('Custom fields', {'fields': ('status','photo','published',)}),
    search_fields = ['username','email','first_name', 'last_name']

admin.site.register(User, MyUserAdmin)
admin.site.register(Permission)
