from django.db import models
from django.contrib.auth.models import User # Importamos el modelo de usuario base de Django

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
    año_estudio = models.IntegerField(blank=True, null=True)
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
    ramo_tutorizado = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ramo de Tutoría/Interés'
    )

    # ... otros campos ...

    # NUEVO CAMPO: Enlace a la sala de chat privada con el tutor
    room_tutor = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estudiantes_de_sala',
        verbose_name="Sala Privada con Tutor"
    )
    def __str__(self):
        # get_rol_display es un método automático de Django que funciona con choices.
        return "{self.user.username} ({self.rol_universitario})"

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salas_como_estudiante', null=True, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salas_como_tutor', null=True, blank=True)

    class Meta:
        unique_together = ('estudiante', 'tutor')

class Mensaje(models.Model):
    # La sala a la que pertenece el mensaje
    sala = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='mensajes')
    
    # El autor del mensaje (User logueado)
    autor = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('timestamp',)
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return f'{self.autor.username}: {self.contenido[:20]}...'

class Marker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='markers')
    lat = models.FloatField()
    lng = models.FloatField()
    popup = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Marcador de {self.user.username} en ({self.lat}, {self.lng})"
