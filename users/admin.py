from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administrador personalizado para usuarios"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'is_active']
    list_filter = ['role', 'is_approved', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('role', 'is_approved', 'telefono')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('role', 'is_approved', 'telefono', 'first_name', 'last_name', 'email')
        }),
    )
