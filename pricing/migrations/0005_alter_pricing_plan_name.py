# Generated by Django 4.2.1 on 2023-06-10 10:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0004_remove_pricing_api_mo_remove_pricing_pricing_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pricing",
            name="plan_name",
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
