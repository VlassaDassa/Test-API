# Generated by Django 4.2.4 on 2023-10-21 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApi', '0003_alter_product_count_feedbacks_alter_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
    ]