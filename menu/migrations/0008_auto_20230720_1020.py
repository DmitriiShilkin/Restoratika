# Generated by Django 3.2 on 2023-07-20 07:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_alter_dish_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='dish',
            name='margin',
        ),
        migrations.AddField(
            model_name='dish',
            name='discount_rub',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AddField(
            model_name='dish',
            name='increment',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AddField(
            model_name='dish',
            name='increment_rub',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.RemoveField(
            model_name='dish',
            name='menu_section',
        ),
        migrations.AddField(
            model_name='dish',
            name='menu_section',
            field=models.ManyToManyField(related_name='dish', to='menu.MenuSection'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='sticker',
            field=models.CharField(choices=[('NEW', 'Новинка'), ('SAL', 'Скидка'), ('TOP', 'Топ продаж'), ('ETY', 'Без отметки')], default='NEW', max_length=3),
        ),
    ]
