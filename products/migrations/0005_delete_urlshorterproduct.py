# Generated by Django 4.2.1 on 2023-05-25 21:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_urlshorterproduct_url_api"),
    ]

    operations = [
        migrations.DeleteModel(
            name="URLShorterProduct",
        ),
    ]
