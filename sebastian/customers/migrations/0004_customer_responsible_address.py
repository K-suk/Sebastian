# Generated by Django 4.2.13 on 2024-06-09 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0003_alter_customer_due"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="responsible_address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
