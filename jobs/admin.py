# job_management/admin.py
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('customer', 'worker', 'status', 'link', 'due')
    list_filter = ('status', 'worker')
    search_fields = ('customer__first_name', 'customer__last_name', 'worker__username', 'link', 'due')
    raw_id_fields = ('customer', 'worker')