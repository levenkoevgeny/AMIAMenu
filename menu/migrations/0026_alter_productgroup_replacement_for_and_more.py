# Generated by Django 4.0.2 on 2022-04-05 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0025_remove_productgroup_replacements_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productgroup',
            name='replacement_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.productgroup', verbose_name='Является заменой для'),
        ),
        migrations.DeleteModel(
            name='ReplacementForProductGroup',
        ),
    ]