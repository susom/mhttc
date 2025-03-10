# Generated by Django 3.2 on 2021-06-08 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_formtemplate_target_audience_relations_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingoutcome',
            name='outcome_results',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formtemplate',
            name='evaluation_planned_enrollment_individual',
            field=models.CharField(blank=True, help_text='How many individual planned for enrollment? (number only)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='formtemplate',
            name='evaluation_planned_enrollment_organization',
            field=models.CharField(blank=True, help_text='How many organization planned for enrollment? (number only)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='formtemplate',
            name='target_audience_relations',
            field=models.IntegerField(blank=True, choices=[(1, 'Single individuals from multiple organizations'), (2, 'Multiple individuals within one organization'), (3, 'Multiple individuals or teams from multiple organizations'), (99, 'Other')], default=1, help_text='Specify audience relationship to one another (Choose one):'),
        ),
    ]
