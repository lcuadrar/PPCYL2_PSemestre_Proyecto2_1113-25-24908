import requests
from django.shortcuts import render, redirect

API_URL = 'http://127.0.0.1:5000'

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasenia = request.POST.get('contrasenia')

        # Le preguntamos a la API si el usuario existe
        respuesta = requests.post(f'{API_URL}/login', json={
            'usuario': usuario,
            'contrasenia': contrasenia
        })

        if respuesta.status_code == 200:
            datos = respuesta.json()
            # Guardamos el usuario y rol en la sesión
            request.session['usuario'] = usuario
            request.session['rol'] = datos['rol']
            return redirect('inicio')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')

def inicio(request):
    rol = request.session.get('rol')
    return render(request, 'inicio.html', {'rol': rol})

def admin_panel(request):
    if request.session.get('rol') != 'administrador':
        return redirect('login')
    return render(request, 'admin_panel.html')

def cargar_xml(request):
    if request.session.get('rol') != 'administrador':
        return redirect('login')
    
    salida = None
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            contenido = archivo.read()
            respuesta = requests.post(
                f'{API_URL}/cargar',
                data=contenido,
                headers={'Content-Type': 'text/xml'}
            )
            salida = respuesta.text

    return render(request, 'cargar_xml.html', {'salida': salida})

def ver_usuarios(request):
    if request.session.get('rol') != 'administrador':
        return redirect('login')
    
    respuesta = requests.get(f'{API_URL}/usuarios')
    usuarios = respuesta.json().get('usuarios', [])
    
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})

def tutor_panel(request):
    if request.session.get('rol') != 'tutor':
        return redirect('login')
    return render(request, 'tutor_panel.html')

def cargar_horarios(request):
    if request.session.get('rol') != 'tutor':
        return redirect('login')
    
    horarios = None
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            contenido = archivo.read()
            respuesta = requests.post(
                f'{API_URL}/horarios',
                data=contenido,
                headers={'Content-Type': 'text/xml'}
            )
            horarios = respuesta.json().get('horarios', [])

    return render(request, 'cargar_horarios.html', {'horarios': horarios})

def cargar_notas(request):
    if request.session.get('rol') != 'tutor':
        return redirect('login')
    
    mensaje = None
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            contenido = archivo.read()
            respuesta = requests.post(
                f'{API_URL}/notas',
                data=contenido,
                headers={'Content-Type': 'text/xml'}
            )
            mensaje = respuesta.json().get('mensaje')

    return render(request, 'cargar_notas.html', {'mensaje': mensaje})

def estudiante_panel(request):
    if request.session.get('rol') != 'estudiante':
        return redirect('login')
    
    carnet = request.session.get('usuario')
    respuesta = requests.get(f'{API_URL}/notas/770/{carnet}')
    notas = respuesta.json().get('notas', [])
    
    return render(request, 'estudiante_panel.html', {'notas': notas, 'carnet': carnet})