# Generated by Django 3.0.6 on 2020-05-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.CharField(max_length=255),
        ),
    ]
