# Generated by Django 4.0.2 on 2022-04-19 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0030_productgroup_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatmentkind',
            name='is_heat_treatment',
        ),
    ]