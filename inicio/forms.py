from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Perfil 


class FormularioRegistro(UserCreationForm):
    # Campos base de Django que queremos recolectar en el registro
    first_name = forms.CharField(label='Nombres', max_length=30)
    last_name = forms.CharField(label='Apellidos', max_length=30)
    email = forms.EmailField(required=True, label='Correo Electrónico')
    
    # CAMPO CRÍTICO: Rol Universitario
    rol_universitario = forms.CharField(
        label='Rol Universitario', 
        max_length=15, 
        help_text='Tu número de identificación universitaria (ej: 123456789-0).'    )
    
    # Campos personalizados del modelo Perfil
    rol = forms.ChoiceField(
        choices=Perfil.OPCIONES_ROL,
        label='¿Eres estudiante o tutor/a?'
    )
    nombre_social = forms.CharField(
        label='Nombre Social', 
        max_length=100, 
        required=False, 
        help_text='Nombre preferido para dirigirse a ti (Opcional).'
    )
    edad = forms.IntegerField(label='Edad', min_value=15)
    carrera = forms.CharField(label='Carrera', max_length=100)
    año_estudio = forms.IntegerField(
    label='Año de Ingreso',
    min_value=2000,
    max_value=2100,
    help_text="Año en que ingresaste a la universidad (ej: 2025)."
)

    class Meta(UserCreationForm.Meta):
        # Aseguramos que los campos base se incluyan en el formulario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)

    @transaction.atomic # Garantiza la integridad de los datos en SQLite
    def save(self, commit=True):
        # 1. Guarda el usuario base (username, password, nombres, email)
        usuario = super().save(commit=False)
        usuario.first_name = self.cleaned_data["first_name"]
        usuario.last_name = self.cleaned_data["last_name"]
        usuario.email = self.cleaned_data["email"]
        
        if commit:
            usuario.save()
            # 2. Crea y guarda el perfil asociado (la conexión One-to-One)
            Perfil.objects.create(
                user=usuario, # CONEXIÓN: user con Perfil
                rol_universitario=self.cleaned_data["rol_universitario"], # Guardamos el Rol
                rol=self.cleaned_data["rol"],
                nombre_social=self.cleaned_data["nombre_social"],
                edad=self.cleaned_data["edad"],
                carrera=self.cleaned_data["carrera"],
                año_estudio=self.cleaned_data["año_estudio"],
            
            )
        return usuario