# Generated by Django 4.2.4 on 2023-10-15 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0021_colormodel_sizemodel_productcharacteristics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcharacteristics',
            name='color',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='productcharacteristics',
            name='size',
            field=models.BooleanField(default=False),
        ),
    ]
