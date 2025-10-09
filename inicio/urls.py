from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'),
    path('mapa/', views.mapa, name='mapa'),
    path('tutores/', views.tutores, name='tutores'),
    path('perfil/', views.perfil, name='perfil'),
]