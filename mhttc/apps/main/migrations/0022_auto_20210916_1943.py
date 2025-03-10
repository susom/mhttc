# Generated by Django 3.2.6 on 2021-09-16 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0021_auto_20210608_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lead', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='formtemplate',
            name='end_date',
            field=models.DateField(help_text='project end date', null=True),
        ),
    ]
