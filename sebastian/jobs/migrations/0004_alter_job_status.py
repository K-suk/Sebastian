# Generated by Django 4.2.13 on 2024-06-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0003_alter_job_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="status",
            field=models.CharField(
                choices=[
                    ("NEW", "New"),
                    ("IN_PROGRESS", "In Progress"),
                    ("EVALUATION", "Under Evaluation"),
                    ("APPROVED", "Approved"),
                    ("IMPROVEMENT", "Improvement Required"),
                    ("COMPLETED", "Completed"),
                ],
                default="NEW",
                max_length=20,
            ),
        ),
    ]
