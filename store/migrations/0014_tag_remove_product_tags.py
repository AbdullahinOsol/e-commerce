# Generated by Django 4.2.16 on 2025-01-02 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
    ]
