# Generated by Django 4.2.4 on 2024-02-10 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0035_alter_onroad_bank_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onroad',
            name='bank_card',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='testApi.bankcards'),
        ),
    ]
