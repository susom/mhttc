# Generated by Django 3.2 on 2021-04-27 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210427_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='strategy',
            old_name='strategy_type_fk',
            new_name='strategy_type',
        ),
    ]
