# Generated by Django 4.2.3 on 2023-12-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userauths", "0003_alter_user_referral_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="deposit",
            name="trx_hash",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]