

from django.contrib import admin
from .models import Perfil # Importamos Perfil
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Clase Inline para mostrar el perfil junto al usuario en el panel de admin de Django
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False 
    verbose_name_plural = 'Perfil de Usuario (Información Extendida)'
    fk_name = 'user' 
    # Agregamos el Rol Universitario para poder verlo fácilmente en el admin
    fields = ('rol_universitario', 'rol', 'nombre_social', 'edad', 'carrera', 'año_estudio', 'tutor')


# Personalizamos la administración del modelo User
class UsuarioAdminPersonalizado(UserAdmin):
    # Inyectamos el PerfilInline en la vista de edición de usuario
    inlines = (PerfilInline,)
    
    # Añadimos el rol a la lista de columnas en el listado de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'obtener_rol')
    
    # Función para obtener y mostrar el rol del perfil
    def obtener_rol(self, objeto):
        try:
            # Usamos el atributo 'perfil' que Django crea por la relación OneToOne
            return objeto.perfil.get_rol_display() 
        except Perfil.DoesNotExist:
            return 'N/A - Perfil Faltante'
    obtener_rol.short_description = 'Rol'

# 1. Desregistramos el modelo User por defecto.
admin.site.unregister(User)
# 2. Registramos la versión personalizada con el perfil incrustado.
admin.site.register(User, UsuarioAdminPersonalizado)

