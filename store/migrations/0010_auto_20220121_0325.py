# Generated by Django 3.2 on 2022-01-21 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20220121_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='description3',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='description1',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
