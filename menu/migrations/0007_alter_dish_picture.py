# Generated by Django 3.2 on 2023-06-30 19:09

from django.db import migrations, models
import menu.models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_dish_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='picture',
            field=models.ImageField(blank=True, upload_to=menu.models.get_image_path),
        ),
    ]