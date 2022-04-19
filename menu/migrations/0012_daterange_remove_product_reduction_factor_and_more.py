# Generated by Django 4.0.2 on 2022-04-02 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0011_productsinmap_dish_category_productsinmap_treatments'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(verbose_name='Начало диапазона')),
                ('date_till', models.DateField(verbose_name='Окончание диапазона')),
            ],
            options={
                'verbose_name': 'Диапазон дат',
                'verbose_name_plural': 'Диапазоны дат',
                'ordering': ('date_from',),
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='reduction_factor',
        ),
        migrations.CreateModel(
            name='WastageByDateRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(verbose_name='Потеря, %')),
                ('date_range', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.daterange', verbose_name='Диапазон дат')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.product', verbose_name='Продукт')),
                ('treatment_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.treatmentkind', verbose_name='Вид обработки')),
            ],
            options={
                'verbose_name': 'Потеря по диапазону дат',
                'verbose_name_plural': 'Потери по диапазону дат',
                'ordering': ('product',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='wastage',
            field=models.ManyToManyField(through='menu.WastageByDateRange', to='menu.DateRange', verbose_name='Потери при обработке'),
        ),
    ]
