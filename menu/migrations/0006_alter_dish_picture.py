# Generated by Django 3.2 on 2023-06-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20230630_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='picture',
            field=models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d'),
        ),
    ]
