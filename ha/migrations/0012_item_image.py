# Generated by Django 2.1.2 on 2018-11-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ha', '0011_auto_20181106_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default=None, upload_to='imgs'),
            preserve_default=False,
        ),
    ]
