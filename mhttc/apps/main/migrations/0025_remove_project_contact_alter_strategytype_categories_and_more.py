# Generated by Django 4.2.6 on 2023-10-26 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_strategytype_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contact',
        ),
        migrations.AlterField(
            model_name='strategytype',
            name='categories',
            field=models.PositiveIntegerField(choices=[(1, 'Change infrastructure'), (2, 'Use financial strategies'), (4, 'Support deliverers of the intervention/program/service'), (5, 'Train and educate stakeholders'), (6, 'Develop stakeholder relationships'), (7, 'Adapt and tailor content'), (8, 'Provide interactive assistance'), (9, 'Use evaluative and iterative strategies'), (0, 'Other')], default=0),
        ),
        migrations.AlterField(
            model_name='training',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trainingparticipant',
            name='name',
            field=models.CharField(max_length=75),
        ),
    ]
