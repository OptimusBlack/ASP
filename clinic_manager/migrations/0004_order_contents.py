# Generated by Django 2.1.2 on 2018-10-30 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_manager', '0003_order_orderstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contents',
            field=models.TextField(default='{}'),
        ),
    ]
