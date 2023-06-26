# Generated by Django 3.2 on 2023-04-07 12:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_table_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='client_email',
            field=models.EmailField(max_length=32, validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='application',
            name='number_persons',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AlterField(
            model_name='application',
            name='time',
            field=models.TimeField(),
        ),
    ]