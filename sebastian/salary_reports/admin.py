from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SalaryReport

@admin.register(SalaryReport)
class SalaryReportAdmin(admin.ModelAdmin):
    list_display = ('worker', 'month', 'year', 'salary', 'penalty', 'job_amount')
    list_filter = ('month', 'year', 'worker')
    search_fields = ('worker__first_name', 'month', 'year')