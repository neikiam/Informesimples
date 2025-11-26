from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from collections import defaultdict
from .models import Report
from .forms import ReportForm
from users.models import CustomUser


@login_required
def empleado_dashboard(request):
    """Dashboard para empleados"""
    if request.user.role != CustomUser.Role.EMPLEADO:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard')
    
    # Informes del empleado
    informes = Report.objects.filter(empleado=request.user).order_by('-fecha_inicio', '-hora_inicio')[:10]
    
    context = {
        'informes': informes,
    }
    
    return render(request, 'reports/empleado_dashboard.html', context)


@login_required
def create_report(request):
    """Vista para crear un nuevo informe de jornada"""
    if request.user.role != CustomUser.Role.EMPLEADO:
        messages.error(request, 'Solo los empleados pueden crear informes.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.empleado = request.user
            report.save()
            messages.success(request, 'Informe de jornada creado exitosamente.')
            return redirect('empleado_dashboard')
    else:
        form = ReportForm()
    
    return render(request, 'reports/create_report.html', {'form': form})


@login_required
def contador_dashboard(request):
    """Dashboard para contador - ver todos los informes"""
    if request.user.role != CustomUser.Role.CONTADOR:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard')
    
    # Todos los informes
    informes = Report.objects.all().select_related('empleado').order_by('-fecha_inicio', '-hora_inicio')
    
    # Empleados
    empleados = CustomUser.objects.filter(
        role=CustomUser.Role.EMPLEADO,
        is_approved=True
    )
    
    context = {
        'informes': informes,
        'empleados': empleados,
    }
    
    return render(request, 'reports/contador_dashboard.html', context)


@login_required
def empleado_performance(request, empleado_id):
    """Vista del rendimiento diario de un empleado específico"""
    if request.user.role != CustomUser.Role.CONTADOR and request.user.role != CustomUser.Role.STAFF:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard')
    
    empleado = get_object_or_404(CustomUser, id=empleado_id, role=CustomUser.Role.EMPLEADO)
    
    # Obtener todos los informes del empleado
    informes = Report.objects.filter(empleado=empleado).order_by('fecha_inicio')
    
    # Agrupar por fecha
    informes_por_fecha = defaultdict(list)
    for informe in informes:
        informes_por_fecha[informe.fecha_inicio].append(informe)
    
    # Calcular resumen por fecha
    resumen_diario = []
    for fecha, informes_dia in sorted(informes_por_fecha.items(), reverse=True):
        datos = Report.calcular_horas_extra_dia(empleado, fecha)
        resumen_diario.append(datos)
    
    context = {
        'empleado': empleado,
        'resumen_diario': resumen_diario,
    }
    
    return render(request, 'reports/empleado_performance.html', context)


@login_required
def report_detail(request, report_id):
    """Vista de detalle de un informe"""
    report = get_object_or_404(Report, id=report_id)
    
    # Solo contador, staff y el empleado propietario pueden ver el informe
    if (request.user.role not in [CustomUser.Role.CONTADOR, CustomUser.Role.STAFF] and 
        request.user != report.empleado):
        messages.error(request, 'No tienes permiso para ver este informe.')
        return redirect('dashboard')
    
    context = {
        'report': report,
    }
    
    return render(request, 'reports/report_detail.html', context)
