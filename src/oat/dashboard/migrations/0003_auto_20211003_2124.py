# Generated by Django 2.2 on 2021-10-03 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_category_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/category/'),
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/menu/'),
        ),
    ]
