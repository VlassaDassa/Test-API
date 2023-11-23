# Generated by Django 4.2.4 on 2023-11-22 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0011_remove_deliverypoints_seleceted'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='testApi.colormodel'),
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='testApi.sizemodel'),
        ),
    ]