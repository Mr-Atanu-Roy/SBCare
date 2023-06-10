# Generated by Django 4.2.1 on 2023-06-10 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0004_remove_pricing_api_mo_remove_pricing_pricing_and_more"),
        ("accounts", "0014_alter_userprofile_plan"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentsHistory",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "payment_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_paid", models.BooleanField(default=False)),
                ("amount", models.CharField(max_length=255)),
                ("purpose", models.CharField(blank=True, max_length=255, null=True)),
                ("phone", models.CharField(blank=True, max_length=12, null=True)),
                ("instamojo_id", models.CharField(max_length=500)),
                (
                    "plan",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pricing.pricing",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
