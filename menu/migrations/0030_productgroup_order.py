# Generated by Django 4.0.2 on 2022-04-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0029_productsinmap_product_count_gross_normalize_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgroup',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Порядковый номер (для вывода в меню)'),
        ),
    ]