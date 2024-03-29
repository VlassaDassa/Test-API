# Generated by Django 4.2.4 on 2024-02-06 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0029_remove_customuser_delivery_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='delivery_point',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='testApi.deliverypoints'),
            preserve_default=False,
        ),
    ]
