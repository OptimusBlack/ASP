# Generated by Django 2.1.2 on 2018-11-18 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_user_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
