# Generated by Django 4.0.2 on 2022-03-22 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_mapsinmenuday_alter_map_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='map_number',
            field=models.CharField(default=1, max_length=100, verbose_name='Номер технологической карты'),
            preserve_default=False,
        ),
    ]