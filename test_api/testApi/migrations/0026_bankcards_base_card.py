# Generated by Django 4.2.4 on 2024-02-02 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0025_alter_deliverypoints_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankcards',
            name='base_card',
            field=models.BooleanField(default=False),
        ),
    ]
