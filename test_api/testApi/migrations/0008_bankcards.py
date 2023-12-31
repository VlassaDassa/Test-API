# Generated by Django 4.2.4 on 2023-09-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0007_andreydelivey'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('main_card', models.BooleanField(default=False)),
            ],
        ),
    ]
