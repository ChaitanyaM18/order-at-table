# Generated by Django 2.2 on 2021-10-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20211023_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='order',
            field=models.TextField(),
        ),
    ]
