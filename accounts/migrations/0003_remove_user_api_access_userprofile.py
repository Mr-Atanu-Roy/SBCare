# Generated by Django 4.2.1 on 2023-05-21 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_api_access"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="api_access",
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                ("auth_token", models.CharField(max_length=500)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("not-specify", "not-specify"),
                        ],
                        default="male",
                        max_length=50,
                    ),
                ),
                ("address1", models.TextField(blank=True, null=True)),
                ("address2", models.TextField(blank=True, null=True)),
                ("coins", models.IntegerField(default=0)),
                ("api_access", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
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
