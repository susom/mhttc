# Generated by Django 3.2 on 2021-04-28 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_strategy_type_fk_strategy_strategy_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formtemplate',
            name='implementation_enrolled',
        ),
        migrations.RemoveField(
            model_name='formtemplate',
            name='implementation_participants',
        ),
        migrations.RemoveField(
            model_name='formtemplate',
            name='implementation_recruited',
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_enrolled_individual',
            field=models.IntegerField(blank=True, help_text='How many individuals enrolled?', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_enrolled_organization',
            field=models.IntegerField(blank=True, help_text='How many organizations enrolled?', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_percent_complete_50_strategy_individual',
            field=models.FloatField(blank=True, help_text='Percentage of individual completing 50% of implementation strategy activities:', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_percent_complete_50_strategy_organization',
            field=models.FloatField(blank=True, help_text='Percentage of Organization completing 50% of implementation strategy activities: ', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_percent_complete_80_strategy_individual',
            field=models.FloatField(blank=True, help_text='Percentage of individual completing 80% or more of implementation strategy activities:', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_percent_complete_80_strategy_organization',
            field=models.FloatField(blank=True, help_text='Percentage of Organization completing 80% or more of implementation strategy activities: ', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_percent_init_implementation_strategy_individual',
            field=models.FloatField(blank=True, help_text='Percentage of individual initiating implementation strategy', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_percent_init_implementation_strategy_organization',
            field=models.FloatField(blank=True, help_text='Percentage of organization initiating implementation strategy', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_planned_enrollment_individual',
            field=models.IntegerField(blank=True, help_text='How many individual planned for enrollment?', null=True),
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_planned_enrollment_organization',
            field=models.IntegerField(blank=True, help_text='How many organization planned for enrollment?', null=True),
        ),
    ]
