# Generated by Django 4.2.13 on 2024-06-08 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0006_job_due"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="due",
            field=models.DateField(blank=True, null=True),
        ),
    ]
