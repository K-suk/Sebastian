from django.db import models

class Customer(models.Model):
    email = models.EmailField(unique=True)  # 顧客のメールアドレス
    first_name = models.CharField(max_length=30)  # 顧客の名
    last_name = models.CharField(max_length=30)  # 顧客の姓
    contact_address = models.CharField(max_length=255)  # 連絡先住所
    task_completed = models.BooleanField(default=False)  # タスク完了フラグ
    task_assigned = models.BooleanField(default=False)  # タスク割り当てフラグ
    due = models.DateField()  # 期限日

    def __str__(self):
        return f"{self.first_name} {self.last_name}"