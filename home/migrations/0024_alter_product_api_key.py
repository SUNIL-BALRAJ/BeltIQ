# Generated by Django 4.2.9 on 2024-04-18 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_product_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='api_key',
            field=models.CharField(max_length=1000),
        ),
    ]
