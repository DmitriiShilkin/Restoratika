# Generated by Django 3.2 on 2023-04-11 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20230408_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='hall',
        ),
        migrations.RemoveField(
            model_name='application',
            name='hall',
        ),
        migrations.RemoveField(
            model_name='application',
            name='table',
        ),
        migrations.DeleteModel(
            name='Hall',
        ),
        migrations.DeleteModel(
            name='Table',
        ),
    ]
