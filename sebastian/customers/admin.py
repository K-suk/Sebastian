from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_address', 'task_completed', 'task_assigned', 'due')
    list_filter = ('task_completed', 'task_assigned', 'due')
    search_fields = ('first_name', 'last_name', 'email')
