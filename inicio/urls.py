from django.urls import path
from . import views 

app_name = 'inicio'

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
    path('chat_lobby/', views.home, name='home'),
    path('room/<int:room_id>/', views.room, name='room'), 
    path('room/<int:room_id>/send/', views.enviar_mensaje, name='enviar_mensaje'),
    path('room/<int:room_id>/messages/', views.obtener_mensajes_ajax, name='obtener_mensajes_ajax'),

    path('api/markers', views.get_markers, name='get_markers'),
    path('api/markers/add', views.add_marker, name='add_marker'),
    path('api/markers/delete/<int:marker_id>/', views.delete_marker, name='delete_marker'),
]
