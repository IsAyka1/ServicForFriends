# Generated by Django 4.2.1 on 2023-05-05 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='users',
        ),
    ]
