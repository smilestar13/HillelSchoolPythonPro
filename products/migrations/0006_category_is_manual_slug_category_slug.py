# Generated by Django 4.2 on 2023-05-18 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_manual_slug',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]