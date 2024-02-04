# Generated by Django 4.2.4 on 2024-01-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0016_onroad_color_onroad_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('seller', models.BooleanField(default=False)),
            ],
        ),
    ]