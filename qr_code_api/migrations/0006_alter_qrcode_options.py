# Generated by Django 4.2.1 on 2023-05-26 05:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("qr_code_api", "0005_alter_qrcode_qr_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="qrcode",
            options={"verbose_name_plural": "QR Code API"},
        ),
    ]
