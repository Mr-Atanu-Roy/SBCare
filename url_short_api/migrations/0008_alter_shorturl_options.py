# Generated by Django 4.2.1 on 2023-05-26 05:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("url_short_api", "0007_alter_shorturl_source"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shorturl",
            options={"verbose_name_plural": "URL Shorter API"},
        ),
    ]
