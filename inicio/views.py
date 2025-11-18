from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login 
from django.contrib.auth.models import User 
from .models import Perfil, Room, Mensaje, Marker 
from .forms import FormularioRegistro 
import random
def asignar_tutor(estudiante_perfil):
    if estudiante_perfil.rol != 'ESTUDIANTE':
        return None
    
    try:
        año_estudiante = int(estudiante_perfil.año_estudio)
    except:
        return None
        
    tutores_candidatos = Perfil.objects.filter(
        rol='TUTOR',
        carrera=estudiante_perfil.carrera
    )

    tutores_validos = []
    for tutor in tutores_candidatos:
        try:
            año_tutor = int(tutor.año_estudio)
        except:
            continue
        if año_tutor < año_estudiante:
            tutores_validos.append(tutor)

    if tutores_validos:
        return random.choice(tutores_validos)
    
    return None

def crear_asignacion_y_sala(estudiante_perfil, tutor_perfil):
    """ Asigna el tutor en el perfil del estudiante y crea la Room privada. """
    
    estudiante_perfil.tutor = tutor_perfil
    estudiante_perfil.save()

    nombre_sala = f"chat_{estudiante_perfil.user.username}_{tutor_perfil.user.username}"

    room, created = Room.objects.get_or_create(
        name=nombre_sala,
        defaults={
            'estudiante': estudiante_perfil.user,
            'tutor': tutor_perfil.user,
        }
    )
    
    if created:
        try:
            Mensaje.objects.create(
                sala=room,
                autor=tutor_perfil.user, 
                contenido="¡Bienvenido al chat!"
            )
        except Exception as e:
            print(f"Error al crear mensaje inicial: {e}")

    print(f"DEBUG: Sala creada? {created} → {room.name}")
    return room

def opciones_inicio_sesion(request):
    """Muestra la página inicial para decidir entre iniciar sesión o registrarse (Caja Central)."""
    if request.user.is_authenticated:
        return redirect('inicio:bienvenida')
        
    return render(request, 'login_options.html', {'title': '¡Bienvenido/a a LIA!'})

def registro_usuario(request):
    """Maneja el formulario de registro y loguea al usuario tras crearlo."""
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            usuario = formulario.save() 
            login(request, usuario) 
            return redirect('inicio:bienvenida')
    else:
        formulario = FormularioRegistro()

    return render(request, 'register.html', {
        'formulario': formulario, 
        'title': 'Regístrate',
    })

vista_login = LoginView.as_view(
    template_name='login.html',
    next_page='inicio:bienvenida'
)

vista_logout = LogoutView.as_view(
    next_page='inicio:opciones_inicio_sesion'
)

@login_required 
def bienvenida(request):
    try:
        perfil_usuario = request.user.perfil
    except Perfil.DoesNotExist:
        return redirect('inicio:perfil')
        
    titulo = f"¡Bienvenido/a, {request.user.first_name}!" 
    
    if perfil_usuario.rol == 'ESTUDIANTE' and perfil_usuario.tutor is None:
        tutor_encontrado = asignar_tutor(perfil_usuario)
        
        if tutor_encontrado:
            try:
                crear_asignacion_y_sala(perfil_usuario, tutor_encontrado)
                print(f"DEBUG: Asignación y sala creadas para {perfil_usuario.user.username}.")
            except Exception as e:
    
                pass
            
    return render(request, 'inicio.html', {'title': titulo})

@login_required 
def mapa(request):
    nombre_mostrar = request.user.first_name
    try:
        if request.user.perfil.nombre_social:
            nombre_mostrar = request.user.perfil.nombre_social
    except:
        pass 
        
    return render(request, 'mapa.html', {'username': nombre_mostrar})

@login_required 
def tutores(request):
    t = "Información de Tutores"
    info_asignacion = 'No se encontraron tutores disponibles'
    
    try:
        perfil = request.user.perfil
        
        if perfil.rol == 'ESTUDIANTE':
            if perfil.tutor:
                usuario_tutor = perfil.tutor.user
                nombre_tutor = usuario_tutor.get_full_name()
                info_asignacion = (
                    f'Tu tutor/a asignado/a es: <strong>{nombre_tutor}</strong>.<br>'
                    f'<span>Rol Universitario: {perfil.tutor.rol_universitario}.</span><br>'
                    f'<span>Contacto: {usuario_tutor.email}.</span>'
                )
            else:
                info_asignacion = 'Aún no tienes un tutor/a asignado/a. Explora los tutores disponibles.'
        elif perfil.rol == 'TUTOR':
            estudiantes = Perfil.objects.filter(tutor=perfil, rol='ESTUDIANTE') 
            if estudiantes.exists():
                nombres_estudiantes = []
                for e in estudiantes:
                    bloque_info = (
                        f"<strong>{e.user.get_full_name()}</strong><br>"
                        f"• Rol: {e.rol_universitario}<br>"
                        f"• Carrera: {e.carrera}"
                    )
                    nombres_estudiantes.append(bloque_info)
                
                lista_estudiantes = ("<hr style='margin: 10px 0;'>").join(nombres_estudiantes)
                info_asignacion = (
                    f"Tienes {estudiantes.count()} estudiante(s) asignado(s):"
                    f"<div style='margin-top: 15px;'>{lista_estudiantes}</div>"
                )
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
        etiqueta_asociado = 'Asociado'
        valor_asociado = 'N/A'
        
        if perfil_usuario.tutor:
            etiqueta_asociado = 'Tutor Asignado'
            if perfil_usuario.tutor:
                valor_asociado = perfil_usuario.tutor.user.get_full_name()
            else:
                valor_asociado = 'Aún no asignado'
        elif perfil_usuario.rol == 'TUTOR':
            estudiantes_asignados = Perfil.objects.filter(tutor=perfil_usuario, rol='ESTUDIANTE')
            
            etiqueta_asociado = 'Estudiantes Asignados'
            if estudiantes_asignados.exists():
                nombres = [e.user.get_full_name() for e in estudiantes_asignados]
                valor_asociado = ' | '.join(nombres) 
            else:
                valor_asociado = 'Ninguno'
            
        datos_perfil = {
            'Rol Universitario': perfil_usuario.rol_universitario, 
            'Nombres': usuario.first_name,
            'Apellidos': usuario.last_name,
            'Nombre Social': perfil_usuario.nombre_social or 'N/A',
            'Edad': perfil_usuario.edad or 'N/A',
            'Carrera': perfil_usuario.carrera or 'N/A',
            'Año de Estudio': perfil_usuario.año_estudio or 'N/A',
            'Rol en el Proyecto': perfil_usuario.get_rol_display(),
            }
        datos_perfil[etiqueta_asociado] = valor_asociado
    except Perfil.DoesNotExist:
        datos_perfil = {'Mensaje': 'Error: Los datos de tu perfil no están disponibles.'}
        
    return render(request, 'perfil.html', { 'p': p, 'datos_perfil': datos_perfil })

def home(request):
    perfil_usuario = request.user.perfil
    salas_autorizadas = []
    
    if perfil_usuario.rol == 'ESTUDIANTE':
        tutor = perfil_usuario.tutor
        if tutor:
            nombre_sala_esperado = f"chat_{request.user.username}_{tutor.user.username}"
            
            try:
                sala = Room.objects.get(name=nombre_sala_esperado)
                salas_autorizadas.append(sala)
            except Room.DoesNotExist:
                pass 
                
    elif perfil_usuario.rol == 'TUTOR':
        estudiantes_asignados = Perfil.objects.filter(tutor=perfil_usuario, rol='ESTUDIANTE')
        
        for estudiante in estudiantes_asignados:
            nombre_sala_esperado = f"chat_{estudiante.user.username}_{perfil_usuario.user.username}"
            
            try:
                sala = Room.objects.get(name=nombre_sala_esperado)
                salas_autorizadas.append(sala)
            except Room.DoesNotExist:
                pass
    
    return render(request, 'chat/home.html', {'rooms': salas_autorizadas})

@login_required
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    perfil_usuario = request.user.perfil
    acceso_permitido = False
    
    if perfil_usuario.rol == 'ESTUDIANTE':
        if perfil_usuario.tutor and perfil_usuario.tutor == room.tutor.perfil:
            acceso_permitido = True
    elif perfil_usuario.rol == 'TUTOR':
        if room.estudiante.perfil.tutor == perfil_usuario:
            acceso_permitido = True
        
    if not acceso_permitido:
        return HttpResponseForbidden("No tienes acceso a esta sala privada.")
    mensajes_antiguos = Mensaje.objects.filter(sala=room).order_by('timestamp')
    
    return render(request, 'chat/room.html', {
        "room": room,
        "mensajes": mensajes_antiguos,
    })

@login_required
def enviar_mensaje(request, room_id):
    if request.method == 'POST':
        try:
            room = get_object_or_404(Room, id=room_id)
            contenido = request.POST.get('contenido') 
            
            if contenido and contenido.strip():
                Mensaje.objects.create(
                    sala=room,
                    autor=request.user,
                    contenido=contenido.strip()
                )
        except Exception as e:
            print(f"Error al guardar mensaje POST: {e}")
        return redirect('inicio:room', room_id=room_id)
    
    return redirect('inicio:home')
@login_required
def obtener_mensajes_ajax(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    mensajes_antiguos = Mensaje.objects.filter(sala=room).order_by('timestamp')
    
    return render(request, 'chat/messages_fragment.html', {
        'mensajes': mensajes_antiguos,
        'current_user_id': request.user.id,
    })



@require_http_methods(["GET"])
def get_markers(request):
    """
    Devuelve los marcadores guardados en la sesión del usuario.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "No autorizado"}, status=401)

    # Obtenemos los marcadores de la base de datos para el usuario actual
    markers = list(Marker.objects.filter(user=request.user).values('id', 'lat', 'lng', 'popup'))
    return JsonResponse(markers, safe=False)

@require_http_methods(["POST"])
def add_marker(request):
    """
    Añade un nuevo marcador a la base de datos, asociado al usuario.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "No autorizado"}, status=401)

    try:
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')

        if lat is None or lng is None:
            return JsonResponse({"error": "Datos inválidos, 'lat' y 'lng' son requeridos."}, status=400)

        # Creamos y guardamos el nuevo marcador en la base de datos
        new_marker = Marker.objects.create(
            user=request.user,
            lat=lat,
            lng=lng,
            popup=data.get('popup', 'Marcador')
        )
        
        # Devolvemos los datos del marcador creado en formato JSON
        response_data = {
            "id": new_marker.id,
            "lat": new_marker.lat,
            "lng": new_marker.lng,
            "popup": new_marker.popup
        }
        return JsonResponse({"status": "success", "marker": response_data}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Cuerpo de la petición inválido."}, status=400)

@require_http_methods(["DELETE"])
@login_required
def delete_marker(request, marker_id):
    """
    Elimina un marcador de la base de datos.
    """
    try:
        # Buscamos el marcador por su ID y nos aseguramos de que pertenezca al usuario actual
        marker = get_object_or_404(Marker, id=marker_id, user=request.user)
        marker.delete()
        return JsonResponse({"status": "success", "message": "Marcador eliminado."})
    except Marker.DoesNotExist:
        # Esto no debería ocurrir si se usa get_object_or_404, pero es una buena práctica
        return JsonResponse({"error": "Marcador no encontrado o no tienes permiso para eliminarlo."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
