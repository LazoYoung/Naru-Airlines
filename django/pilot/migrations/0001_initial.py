# Generated by Django 5.0.6 on 2024-07-20 09:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pilot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simbrief_id', models.CharField(max_length=32)),
                ('acars_api', models.CharField(max_length=255, unique=True)),
                ('greetings', models.CharField(max_length=128)),
                ('livestream_url', models.CharField(max_length=255)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]