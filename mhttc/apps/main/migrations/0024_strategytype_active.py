# Generated by Django 3.2.6 on 2021-11-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_strategytype_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategytype',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
