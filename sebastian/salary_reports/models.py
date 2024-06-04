from django.db import models
from django.conf import settings

class SalaryReport(models.Model):
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    salary = models.IntegerField()
    penalty = models.IntegerField()
    job_amount = models.IntegerField()

    def __str__(self):
        return f"Salary Report for {self.worker.first_name} {self.worker.last_name} - {self.month}/{self.year}"
