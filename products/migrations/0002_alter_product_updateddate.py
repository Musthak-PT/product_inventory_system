# Generated by Django 5.0.6 on 2024-07-18 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='UpdatedDate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
