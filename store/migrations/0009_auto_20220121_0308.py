# Generated by Django 3.2 on 2022-01-21 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='description2',
        ),
        migrations.AddField(
            model_name='product',
            name='description1',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]