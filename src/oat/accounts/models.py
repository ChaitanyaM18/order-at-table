from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
# Create your models here.

STATUS_CHOICES = (
    ("Active", "Active"),
    ("Inactive", "Inactive"),
)

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
# Group.add_to_class('status', models.CharField(
#     max_length=13, choices=STATUS_CHOICES, default='Active'))
Group.add_to_class('role_status', models.CharField(
max_length=13, choices=STATUS_CHOICES, default='Active'))
#Group.add_to_class('users', models.IntegerField(_('Total Users'), default=True))
Permission.add_to_class('required',models.BooleanField(_('Required'), default=True))


class User(AbstractUser):
    groups = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, related_name="groups")
    phone = models.CharField(max_length=13, null=True, blank=True)
    photo = models.FileField(
        upload_to='uploads/users/profile', null=True, blank=True)

    # common fields detail
    status = models.CharField(
        max_length=13, choices=STATUS_CHOICES, default='Inactive')

    created_on = models.DateTimeField(_('Created Date'), auto_now_add=True)
    updated_on = models.DateTimeField(_('Updated Date'), auto_now=True)
    published = models.BooleanField(_('Published on'), default=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'


    def __str__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.first_name:
            return "%s" % (self.first_name)
        else:
            return "%s" % (self.username)
