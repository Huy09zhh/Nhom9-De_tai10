# Generated by Django 5.0 on 2025-02-15 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_product_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='detail',
        ),
    ]
