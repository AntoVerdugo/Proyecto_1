from django.shortcuts import render
from django.http import HttpResponse

def bienvenida(request):
    title = "Proyecto Inicial"
    return render(request, 'inicio.html', { 
        'title': title
    })

def mapa(request): 
     
    username = 'Antonia'
    return render(request, 'mapa.html', { 
        'username': username
    })


def tutores(request):
    t = "Este es tu tutor asignado"
    return render(request, 'tutores.html', { 
        't': t
    })

def perfil(request):
    p = "Este es tu perfil de usuario"
    return render(request, 'perfil.html', { 
        'p': p
    })