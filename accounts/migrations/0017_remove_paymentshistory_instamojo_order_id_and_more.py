# Generated by Django 4.2.1 on 2023-06-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0016_alter_paymentshistory_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentshistory",
            name="instamojo_order_id",
        ),
        migrations.RemoveField(
            model_name="paymentshistory",
            name="instamojo_payment_id",
        ),
        migrations.AddField(
            model_name="paymentshistory",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=1,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="paymentshistory",
            name="order_id",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="paymentshistory",
            name="payment_id",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
