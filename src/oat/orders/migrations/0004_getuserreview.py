# Generated by Django 3.2.8 on 2021-10-14 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_userorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetUserReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.CharField(max_length=5)),
                ('comments', models.TextField()),
            ],
        ),
    ]
