# Generated by Django 4.2.1 on 2023-05-25 21:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("qr_code_api", "0003_alter_qrcode_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="qrcode",
            name="source",
            field=models.CharField(
                choices=[
                    ("api-service", "API Service"),
                    ("sbcare-product", "SB Care Product"),
                ],
                default="api-service",
                max_length=255,
            ),
        ),
    ]