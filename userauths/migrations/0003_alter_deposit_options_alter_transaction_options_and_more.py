# Generated by Django 4.2.3 on 2024-01-03 14:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userauths", "0002_transaction_plan_interval_processed"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="deposit",
            options={"verbose_name": "Users Deposit"},
        ),
        migrations.AlterModelOptions(
            name="transaction",
            options={"verbose_name_plural": "Users that invested"},
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "Profitopit User"},
        ),
        migrations.AddField(
            model_name="transaction",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
