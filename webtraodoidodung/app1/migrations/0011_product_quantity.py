# Generated by Django 5.0 on 2025-02-16 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_product_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
