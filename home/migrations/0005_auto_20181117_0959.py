# Generated by Django 2.1.2 on 2018-11-17 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_registrationtokens'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RegistrationTokens',
            new_name='RegistrationToken',
        ),
    ]