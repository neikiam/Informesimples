from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado con roles y aprobación"""
    
    class Role(models.TextChoices):
        STAFF = 'STAFF', 'Staff'
        CONTADOR = 'CONTADOR', 'Contador'
        EMPLEADO = 'EMPLEADO', 'Empleado'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLEADO,
        verbose_name='Rol'
    )
    
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Aprobado',
        help_text='Usuario aprobado por staff'
    )
    
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # Si es staff, aprobar automáticamente
        if self.role == self.Role.STAFF:
            self.is_approved = True
            self.is_staff = True
        super().save(*args, **kwargs)
