# Generated by Django 2.1.2 on 2018-11-02 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ha', '0002_auto_20181101_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='category',
            field=models.CharField(default='', max_length=200),
        ),
    ]
