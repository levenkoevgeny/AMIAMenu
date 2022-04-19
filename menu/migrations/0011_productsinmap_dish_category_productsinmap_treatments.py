# Generated by Django 4.0.2 on 2022-04-01 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_dishcategory_treatmentkind'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsinmap',
            name='dish_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='menu.dishcategory', verbose_name='Категория блюда'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsinmap',
            name='treatments',
            field=models.ManyToManyField(to='menu.TreatmentKind', verbose_name='Обработки продукта'),
        ),
    ]
