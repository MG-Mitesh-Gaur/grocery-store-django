# Generated by Django 4.0.2 on 2022-03-01 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_category_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('catName', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='cate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category'),
        ),
    ]