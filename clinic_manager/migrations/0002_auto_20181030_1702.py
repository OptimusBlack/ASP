# Generated by Django 2.1.2 on 2018-10-30 17:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='clientId',
        ),
        migrations.AlterField(
            model_name='order',
            name='orderId',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
