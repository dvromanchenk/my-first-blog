# Generated by Django 2.0.13 on 2019-06-12 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='data_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
