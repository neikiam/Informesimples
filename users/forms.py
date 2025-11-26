from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    """Formulario de registro de usuario"""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nombre de usuario',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'


class UserApprovalForm(forms.ModelForm):
    """Formulario para aprobar usuarios y asignar roles"""
    
    class Meta:
        model = CustomUser
        fields = ['role', 'is_approved']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'role': 'Rol',
            'is_approved': 'Usuario aprobado',
        }
