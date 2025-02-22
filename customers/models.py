from django.db import models

class Customer(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_address = models.CharField(max_length=255)
    task_completed = models.BooleanField(default=False)
    task_assigned = models.BooleanField(default=False)
    due = models.DateField()
    responsible_address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"