

from django.db import models
from django.contrib.auth.models import User # Importamos el modelo de usuario base de Django

# =====================================================================
# MODELO DE PERFIL (CONEXIÓN Y ASIGNACIÓN)
# =====================================================================

class Perfil(models.Model):
    # Opciones de rol
    OPCIONES_ROL = [
        ('ESTUDIANTE', 'Estudiante'),
        ('TUTOR', 'Tutor/a'),
    ]

    # CONEXIÓN: Relación Uno-a-Uno con el Usuario Base de Django.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # NUEVO CAMPO: Rol Universitario (ÚNICO para identificación)
    rol_universitario = models.CharField(
        max_length=15, 
        unique=True, 
        verbose_name='Rol Universitario'
    )
    
    # Datos Adicionales
    rol = models.CharField(max_length=15, choices=OPCIONES_ROL, verbose_name='Rol')
    nombre_social = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombre Social')
    edad = models.IntegerField(blank=True, null=True, verbose_name='Edad')
    carrera = models.CharField(max_length=100, blank=True, null=True, verbose_name='Carrera')
    año_estudio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Año de Estudio')
    
    # ASIGNACIÓN: Campo recursivo a sí mismo para conectar Tutor/Estudiante.
    tutor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='estudiantes_asignados', 
        limit_choices_to={'rol': 'TUTOR'}, 
        verbose_name='Tutor Asignado'
    )

    def __str__(self):
        # get_rol_display es un método automático de Django que funciona con choices.
        return f"{self.user.username} ({self.rol_universitario})"