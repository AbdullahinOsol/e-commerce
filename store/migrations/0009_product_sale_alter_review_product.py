# Generated by Django 4.2.16 on 2024-11-22 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_alter_product_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sale",
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2),
        ),
        migrations.AlterField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="store.product",
            ),
        ),
    ]
