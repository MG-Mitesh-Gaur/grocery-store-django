# Generated by Django 4.0.2 on 2022-02-28 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
