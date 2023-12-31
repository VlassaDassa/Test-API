# Generated by Django 4.2.4 on 2023-09-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0005_category_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images/delivery_point')),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('schedule', models.CharField(max_length=50)),
                ('rating', models.IntegerField()),
                ('coord_x', models.FloatField()),
                ('coord_y', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.FileField(upload_to='images/category_icon'),
        ),
    ]
