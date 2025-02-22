from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

class UserAdmin(BaseUserAdmin):
    # フィールドの表示設定
    list_display = ('account_id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('account_id', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'tel', 'contact_address', 'shift_count', 'shift_assigned', 'shift_assigned_done', 'worker_credit', 'ready')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'email', 'first_name', 'last_name', 'tel', 'contact_address', 'shift_count', 'shift_assigned', 'shift_assigned_done', 'worker_credit', 'ready', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('account_id', 'email', 'first_name', 'last_name')
    ordering = ('account_id',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)