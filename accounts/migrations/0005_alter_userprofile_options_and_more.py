# Generated by Django 4.2.1 on 2023-05-26 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_userprofile_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userprofile",
            options={"verbose_name_plural": "User Profile"},
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="auth_token",
        ),
        migrations.CreateModel(
            name="OTP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "otp",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "purpose",
                    models.CharField(
                        choices=[
                            ("email_verify", "email_verify"),
                            ("reset_password", "reset_password"),
                        ],
                        default="email_verify",
                        max_length=255,
                    ),
                ),
                ("if_used", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
