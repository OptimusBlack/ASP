# Generated by Django 2.1.2 on 2018-11-02 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DispatchQueue',
        ),
    ]