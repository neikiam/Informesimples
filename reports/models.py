from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Sum


class Report(models.Model):
    """Modelo para informes de jornada laboral"""
    
    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='informes',
        verbose_name='Empleado'
    )
    
    lugar_evento = models.CharField(
        max_length=500,
        verbose_name='Lugar y dirección de evento'
    )
    
    fecha_inicio = models.DateField(
        verbose_name='Fecha de inicio'
    )
    
    hora_inicio = models.IntegerField(
        choices=[(i, f"{i:02d}:00") for i in range(24)],
        verbose_name='Hora de inicio'
    )
    
    fecha_fin = models.DateField(
        verbose_name='Fecha de finalización'
    )
    
    hora_fin = models.IntegerField(
        choices=[(i, f"{i:02d}:00") for i in range(24)],
        verbose_name='Hora de finalización'
    )
    
    horas_trabajadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        default=0,
        verbose_name='Horas trabajadas'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        verbose_name = 'Informe de jornada'
        verbose_name_plural = 'Informes de jornada'
        ordering = ['-fecha_inicio', '-hora_inicio']
    
    def __str__(self):
        return f"{self.empleado.get_full_name()} - {self.fecha_inicio} ({self.horas_trabajadas}h)"
    
    def save(self, *args, **kwargs):
        # Calcular horas trabajadas
        self.horas_trabajadas = self.calcular_horas()
        super().save(*args, **kwargs)
    
    def calcular_horas(self):
        """Calcula las horas trabajadas entre inicio y fin"""
        inicio = datetime.combine(self.fecha_inicio, datetime.min.time().replace(hour=self.hora_inicio))
        fin = datetime.combine(self.fecha_fin, datetime.min.time().replace(hour=self.hora_fin))
        
        # Si la hora de fin es 0, se considera el final del día anterior
        if self.hora_fin == 0 and self.fecha_fin > self.fecha_inicio:
            fin = datetime.combine(self.fecha_fin, datetime.min.time())
        
        diferencia = fin - inicio
        horas = diferencia.total_seconds() / 3600
        return max(0, horas)  # No permitir horas negativas
    
    @staticmethod
    def calcular_horas_extra_dia(empleado, fecha):
        """
        Calcula las horas extra para un empleado en una fecha específica.
        Horas regulares: 8 horas por día
        Horas extra: cualquier hora por encima de 8
        """
        informes_dia = Report.objects.filter(
            empleado=empleado,
            fecha_inicio=fecha
        )
        
        total_horas = informes_dia.aggregate(
            total=Sum('horas_trabajadas')
        )['total'] or 0
        
        horas_regulares = min(8, float(total_horas))
        horas_extra = max(0, float(total_horas) - 8)
        
        return {
            'fecha': fecha,
            'total_horas': float(total_horas),
            'horas_regulares': horas_regulares,
            'horas_extra': horas_extra,
            'informes': informes_dia
        }
