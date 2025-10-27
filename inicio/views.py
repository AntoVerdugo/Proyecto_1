# inicio/views.py

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login 
from .models import Perfil # Asume que Perfil está en models.py
from .forms import FormularioRegistro # Asume que FormularioRegistro está en forms.py

# ----------------------------------------------------------------------
# VISTAS DE AUTENTICACIÓN (Restablecidas para la Caja Central)
# ----------------------------------------------------------------------

# Vista Principal (Ruta '/')
def opciones_inicio_sesion(request):
    """Muestra la página inicial para decidir entre iniciar sesión o registrarse (Caja Central)."""
    if request.user.is_authenticated:
        return redirect('bienvenida') # Si ya está logueado, va al home
        
    # Muestra el template que contiene la caja central con los dos botones
    return render(request, 'login_options.html', {
        'title': '¡Bienvenido/a a Mi Proyecto!',
    })

# Vista de Registro (Ruta '/registro/')
def registro_usuario(request):
    """Maneja el formulario de registro y loguea al usuario tras crearlo."""
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            usuario = formulario.save() 
            login(request, usuario) 
            return redirect('bienvenida')
    else:
        formulario = FormularioRegistro()
        
    return render(request, 'register.html', {
        'formulario': formulario, 
        'title': 'Regístrate',
    })

# Vista de Login (Usamos la vista genérica de Django)
vista_login = LoginView.as_view(
    template_name='login.html',
    next_page='bienvenida' # Redirige al home si es exitoso
)

# Vista de Logout (Usamos la vista genérica de Django)
vista_logout = LogoutView.as_view(
    next_page='opciones_inicio_sesion' # Redirige a la caja central después de cerrar sesión
)

# ----------------------------------------------------------------------
# VISTAS PROTEGIDAS 
# ----------------------------------------------------------------------

@login_required 
def bienvenida(request):
    titulo = f"¡Bienvenido/a, {request.user.first_name}!" 
    return render(request, 'inicio.html', { 
        'title': titulo
    }) 

# ... (El resto de las funciones: mapa, tutores, perfil, ya están correctas)
@login_required 
def mapa(request):
    nombre_mostrar = request.user.first_name
    try:
        if request.user.perfil.nombre_social:
            nombre_mostrar = request.user.perfil.nombre_social
    except:
        pass 
        
    return render(request, 'mapa.html', { 
        'username': nombre_mostrar 
    }) 

@login_required 
def tutores(request):
    t = "Información de Asignación"
    info_asignacion = 'No se encontró información de asignación.'
    
    try:
        perfil = request.user.perfil
        if perfil.rol == 'ESTUDIANTE':
            if perfil.tutor:
                usuario_tutor = perfil.tutor.user
                nombre_tutor = usuario_tutor.get_full_name()
                info_asignacion = f'Tu tutor/a asignado/a es: {nombre_tutor}. Rol: {perfil.tutor.rol_universitario}. Contacto: {usuario_tutor.email}.'
            else:
                info_asignacion = 'Aún no tienes un tutor/a asignado/a. El departamento de inclusión lo hará pronto.'
        elif perfil.rol == 'TUTOR':
            estudiantes = perfil.estudiantes_asignados.all() 
            if estudiantes.exists():
                nombres_estudiantes = [f"{e.user.get_full_name()} (Rol: {e.rol_universitario}, Carrera: {e.carrera})" for e in estudiantes]
                lista_estudiantes = "<br>".join([f"• {nombre}" for nombre in nombres_estudiantes])
                info_asignacion = f"Tienes {estudiantes.count()} estudiante(s) asignado(s):<br><br>{lista_estudiantes}"
            else:
                info_asignacion = "Actualmente no tienes estudiantes asignados."
    except Perfil.DoesNotExist:
        info_asignacion = "Tu perfil no está completo. Contacta a soporte."

    return render(request, 'tutores.html', { 't': t, 'info_asignacion': info_asignacion }) 

@login_required 
def perfil(request):
    p = "Tu Perfil de Usuario"
    try:
        usuario = request.user
        perfil_usuario = usuario.perfil
        datos_perfil = {
            'Rol Universitario': perfil_usuario.rol_universitario, 
            'Nombres': usuario.first_name,
            'Apellidos': usuario.last_name,
            'Nombre Social': perfil_usuario.nombre_social or 'N/A',
            'Edad': perfil_usuario.edad or 'N/A',
            'Carrera': perfil_usuario.carrera or 'N/A',
            'Año de Estudio': perfil_usuario.año_estudio or 'N/A',
            'Rol en el Proyecto': perfil_usuario.get_rol_display(),
            'Tutor Asignado': perfil_usuario.tutor.user.get_full_name() if perfil_usuario.tutor else 'N/A'
        }
    except Perfil.DoesNotExist:
        datos_perfil = {'Mensaje': 'Error: Los datos de tu perfil no están disponibles.'}
        
    return render(request, 'perfil.html', { 'p': p, 'datos_perfil': datos_perfil })