# Generated by Django 4.0.2 on 2022-04-04 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0019_remove_product_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsinmap',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.productgroup', verbose_name='Группа продуктов'),
        ),
    ]