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
        ('Personal info', {'fields': ('first_name', 'last_name', 'tel', 'contact_address', 'shift_count', 'ready')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # 'created_at' を除外
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'email', 'first_name', 'last_name', 'tel', 'contact_address', 'shift_count', 'ready', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # これを追加
    search_fields = ('account_id', 'email', 'first_name', 'last_name')
    ordering = ('account_id',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします