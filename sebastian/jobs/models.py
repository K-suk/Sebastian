# job_management/models.py
from django.db import models
from django.conf import settings
from customers.models import Customer  # Customerモデルがあるアプリケーションからインポート

class Job(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('EVALUATION', 'Under Evaluation'),
        ('COMPLETED', 'Completed'),
    ]
    
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    approved = models.BooleanField(default=False)
    link = models.URLField()

    def __str__(self):
        return f"Job for {self.customer.first_name} {self.customer.last_name} by {self.worker.username}"
