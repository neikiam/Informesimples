from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    """Formulario simple para crear informes de jornada"""
    
    class Meta:
        model = Report
        fields = ['lugar_evento', 'fecha_inicio', 'hora_inicio', 'fecha_fin', 'hora_fin']
        widgets = {
            'lugar_evento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Oficina Central - Av. Principal 123, Quito'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_inicio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_fin': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'lugar_evento': 'Lugar y dirección de evento',
            'fecha_inicio': 'Fecha de inicio',
            'hora_inicio': 'Hora de inicio',
            'fecha_fin': 'Fecha de finalización',
            'hora_fin': 'Hora de finalización',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        hora_inicio = cleaned_data.get('hora_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        hora_fin = cleaned_data.get('hora_fin')
        
        if fecha_inicio and fecha_fin and hora_inicio is not None and hora_fin is not None:
            from datetime import datetime
            inicio = datetime.combine(fecha_inicio, datetime.min.time().replace(hour=hora_inicio))
            fin = datetime.combine(fecha_fin, datetime.min.time().replace(hour=hora_fin))
            
            # Permitir que hora_fin sea 0 (medianoche) del día siguiente
            if hora_fin == 0 and fecha_fin > fecha_inicio:
                fin = datetime.combine(fecha_fin, datetime.min.time())
            
            if fin <= inicio and not (hora_fin == 0 and fecha_fin > fecha_inicio):
                raise forms.ValidationError(
                    'La fecha y hora de finalización debe ser posterior a la de inicio.'
                )
        
        return cleaned_data
