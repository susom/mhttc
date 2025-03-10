# Generated by Django 3.2.6 on 2021-11-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20210916_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategytype',
            name='categories',
            field=models.PositiveIntegerField(choices=[(0, 'Other'), (1, 'Change infrastructure'), (2, 'Use financial strategies'), (3, 'Engage consumers'), (4, 'Support deliverers of the intervention/program/service'), (5, 'Train and educate stakeholders'), (6, 'Develop stakeholder relationships'), (7, 'Adapt and tailor content'), (8, 'Provide interactive assistance'), (9, 'Use evaluative and iterative strategies')], default=0),
        ),
    ]
