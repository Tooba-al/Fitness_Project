# Generated by Django 4.1.4 on 2023-01-17 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_diet_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='member',
        ),
    ]