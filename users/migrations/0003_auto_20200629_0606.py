# Generated by Django 3.0.6 on 2020-06-29 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(default='user_account_outdated', unique=True),
        ),
    ]
