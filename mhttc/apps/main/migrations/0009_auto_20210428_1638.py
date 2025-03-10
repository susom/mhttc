# Generated by Django 3.2 on 2021-04-28 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210428_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome', models.TextField(blank=True, null=True)),
                ('how_outcome_measured', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='formtemplate',
            name='target_audience_across_orgs',
        ),
        migrations.RemoveField(
            model_name='formtemplate',
            name='target_audience_teams_across_orgs',
        ),
        migrations.RemoveField(
            model_name='formtemplate',
            name='target_audience_within_org',
        ),
        migrations.AddField(
            model_name='formtemplate',
            name='evaluation_proximal_training_outcome',
            field=models.ManyToManyField(blank=True, default=None, related_name='form_training_outcome', related_query_name='form_training_outcome', to='main.TrainingOutcome'),
        ),
    ]
