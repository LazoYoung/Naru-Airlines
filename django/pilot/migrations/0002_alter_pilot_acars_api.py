# Generated by Django 5.0.6 on 2024-07-24 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pilot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='acars_api',
            field=models.CharField(max_length=255),
        ),
    ]