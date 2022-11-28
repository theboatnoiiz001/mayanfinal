# Generated by Django 2.2.24 on 2022-03-08 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appearance', '0013_theme_font_size_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='font_size_menu',
            field=models.IntegerField(default=15, help_text='Font size menu.', verbose_name='Font size menu'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='font_size_header',
            field=models.IntegerField(default=19, help_text='Font size header brand.', verbose_name='Font size brand'),
        ),
    ]