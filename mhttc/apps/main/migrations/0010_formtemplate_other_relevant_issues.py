# Generated by Django 3.2 on 2021-04-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210428_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='formtemplate',
            name='other_relevant_issues',
            field=models.TextField(blank=True, help_text='Other relevant issues?', null=True),
        ),
    ]
