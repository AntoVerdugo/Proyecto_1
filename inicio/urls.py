# inicio/urls.py

from django.urls import path
from . import views

# Importamos solo las vistas que son variables (no funciones 'def')
from .views import vista_login, vista_logout, registro_usuario 

urlpatterns = [
    # RUTA PRINCIPAL: Mapea '/' a la vista que muestra los botones (Caja Central)
    path('', views.opciones_inicio_sesion, name='opciones_inicio_sesion'), 
    
    # Rutas de Autenticación
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('registro/', views.registro_usuario, name='registro'), 
    
    # Rutas Protegidas (Contenido de la web)
    # Home principal de la web, accesible solo si está logueado
    path('bienvenida/', views.bienvenida, name='bienvenida'), 
    path('mapa/', views.mapa, name='mapa'),
    path('tutores/', views.tutores, name='tutores'),
    path('perfil/', views.perfil, name='perfil'),
]