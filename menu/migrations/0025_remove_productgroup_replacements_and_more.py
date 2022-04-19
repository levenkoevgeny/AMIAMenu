# Generated by Django 4.0.2 on 2022-04-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0024_replacementforproductgroup_productgroup_replacements_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productgroup',
            name='replacements',
        ),
        migrations.AddField(
            model_name='productgroup',
            name='in_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Норма по замене на 100 г. основного продукта'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='norm_per_day',
            field=models.FloatField(blank=True, null=True, verbose_name='Норма на одного человека в сутки (брутто, грамм)'),
        ),
        migrations.AlterField(
            model_name='replacementforproductgroup',
            name='in_count',
            field=models.IntegerField(verbose_name='Норма по замене на 100 г. продукта'),
        ),
    ]
