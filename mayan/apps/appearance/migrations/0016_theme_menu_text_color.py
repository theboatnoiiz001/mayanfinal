# Generated by Django 2.2.24 on 2022-03-08 06:57

import colorful.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appearance', '0015_theme_font_size_content_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='menu_text_color',
            field=colorful.fields.RGBColorField(blank=True, help_text='Menu text color.', verbose_name='Menu text color'),
        ),
    ]
