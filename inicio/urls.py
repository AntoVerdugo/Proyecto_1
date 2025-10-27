

from django.urls import path
from . import views 

urlpatterns = [
    # RUTA PRINCIPAL: Mapea '/' a la vista que muestra los botones (Caja Central)
    path('', views.opciones_inicio_sesion, name='opciones_inicio_sesion'), 
    
    # Rutas de Autenticación
    # Accedemos a las vistas a través del módulo views.
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'), 
    path('registro/', views.registro_usuario, name='registro'), 
    
    # Rutas Protegidas (Contenido de la web)
    path('bienvenida/', views.bienvenida, name='bienvenida'), 
    path('mapa/', views.mapa, name='mapa'),
    path('tutores/', views.tutores, name='tutores'),
    path('perfil/', views.perfil, name='perfil'),
]