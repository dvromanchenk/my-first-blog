# Generated by Django 2.0.13 on 2019-06-13 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190612_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reason',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirm',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]