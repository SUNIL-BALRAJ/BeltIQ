# Generated by Django 3.2.16 on 2023-08-24 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20230824_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisresult',
            name='channel_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='analysisresult',
            name='promotion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
