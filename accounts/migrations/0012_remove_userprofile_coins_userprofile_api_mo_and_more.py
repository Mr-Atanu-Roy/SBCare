# Generated by Django 4.2.1 on 2023-06-10 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0001_initial"),
        ("accounts", "0011_alter_usertoken_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="coins",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="api_mo",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="last_paid",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="plan",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pricing.pricing",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="qr_mo",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="url_mo",
            field=models.IntegerField(default=0),
        ),
    ]