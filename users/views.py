from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserRegistrationForm, UserApprovalForm
from .models import CustomUser


def register(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Requiere aprobación
            user.save()
            messages.success(
                request,
                'Registro exitoso. Tu cuenta está pendiente de aprobación por el personal administrativo.'
            )
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard principal que redirige según el rol del usuario"""
    user = request.user
    
    # Verificar si el usuario está aprobado
    if not user.is_approved and user.role != CustomUser.Role.STAFF:
        messages.warning(request, 'Tu cuenta aún no ha sido aprobada.')
        return render(request, 'users/pending_approval.html')
    
    # Redirigir según el rol
    if user.role == CustomUser.Role.STAFF:
        return redirect('staff_dashboard')
    elif user.role == CustomUser.Role.CONTADOR:
        return redirect('contador_dashboard')
    elif user.role == CustomUser.Role.EMPLEADO:
        return redirect('empleado_dashboard')
    
    return render(request, 'users/dashboard.html')


@login_required
def staff_dashboard(request):
    """Dashboard para usuarios Staff"""
    if request.user.role != CustomUser.Role.STAFF:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard')
    
    # Usuarios pendientes de aprobación
    pending_users = CustomUser.objects.filter(is_approved=False).exclude(role=CustomUser.Role.STAFF)
    
    # Todos los usuarios
    all_users = CustomUser.objects.all().order_by('-date_joined')
    
    context = {
        'pending_users': pending_users,
        'all_users': all_users,
    }
    
    return render(request, 'users/staff_dashboard.html', context)


@login_required
def approve_user(request, user_id):
    """Vista para aprobar usuarios y asignar roles"""
    if request.user.role != CustomUser.Role.STAFF:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserApprovalForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {user.username} actualizado correctamente.')
            return redirect('staff_dashboard')
    else:
        form = UserApprovalForm(instance=user)
    
    context = {
        'form': form,
        'user_to_approve': user,
    }
    
    return render(request, 'users/approve_user.html', context)
