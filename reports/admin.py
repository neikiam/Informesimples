from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Administrador para informes de jornada"""
    
    list_display = ['empleado', 'lugar_evento', 'fecha_inicio', 'hora_inicio', 'fecha_fin', 'hora_fin', 'horas_trabajadas', 'created_at']
    list_filter = ['fecha_inicio', 'empleado']
    search_fields = ['empleado__username', 'empleado__first_name', 'empleado__last_name', 'lugar_evento']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['horas_trabajadas', 'created_at']
