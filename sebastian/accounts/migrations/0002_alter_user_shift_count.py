# Generated by Django 4.2.13 on 2024-05-28 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="shift_count",
            field=models.IntegerField(default=0, verbose_name="shift_count"),
        ),
    ]
