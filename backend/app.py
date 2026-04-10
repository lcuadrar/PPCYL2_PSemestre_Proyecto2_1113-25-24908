from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from matriz import MatrizDispersa
import re

app = Flask(__name__)

# Aquí guardaremos todos los datos en memoria
usuarios = []
cursos = []
tutores = []
estudiantes = []
notas = {}

@app.route('/')
def index():
    return 'API de AcadNet funcionando!'
@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    usuario = datos.get('usuario')
    contrasenia = datos.get('contrasenia')

    # Verificar si es el administrador
    if usuario == 'AdminPPCYL2' and contrasenia == 'AdminPPCYL2771':
        return jsonify({'mensaje': 'Login exitoso', 'rol': 'administrador'})

    # Buscar en la lista de usuarios
    for u in usuarios:
        if u['usuario'] == usuario and u['contrasenia'] == contrasenia:
            return jsonify({'mensaje': 'Login exitoso', 'rol': u['rol']})

    return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401

@app.route('/cargar', methods=['POST'])
def cargar_xml():
    archivo = request.data.decode('utf-8')
    
    try:
        root = ET.fromstring(archivo)
    except:
        return jsonify({'mensaje': 'XML inválido'}), 400

    # Limpiar datos anteriores
    cursos.clear()
    tutores.clear()
    estudiantes.clear()

    # Cargar cursos
    for curso in root.find('cursos'):
        cursos.append({
            'codigo': curso.get('codigo'),
            'nombre': curso.text
        })

    # Cargar tutores
    for tutor in root.find('tutores'):
        tutores.append({
            'usuario': tutor.get('registro_personal'),
            'contrasenia': tutor.get('contrasenia'),
            'nombre': tutor.text,
            'rol': 'tutor'
        })
        usuarios.append({
            'usuario': tutor.get('registro_personal'),
            'contrasenia': tutor.get('contrasenia'),
            'rol': 'tutor'
        })

    # Cargar estudiantes
    for estudiante in root.find('estudiantes'):
        estudiantes.append({
            'usuario': estudiante.get('carnet'),
            'contrasenia': estudiante.get('contrasenia'),
            'nombre': estudiante.text,
            'rol': 'estudiante'
        })
        usuarios.append({
            'usuario': estudiante.get('carnet'),
            'contrasenia': estudiante.get('contrasenia'),
            'rol': 'estudiante'
        })

    return jsonify({
        'mensaje': 'Datos cargados correctamente',
        'cursos': len(cursos),
        'tutores': len(tutores),
        'estudiantes': len(estudiantes)
    })
@app.route('/notas', methods=['POST'])
def cargar_notas():
    archivo = request.data.decode('utf-8')
    
    try:
        root = ET.fromstring(archivo)
    except:
        return jsonify({'mensaje': 'XML inválido'}), 400

    codigo_curso = root.get('codigo')
    
    # Si no existe la matriz para ese curso, la creamos
    if codigo_curso not in notas:
        notas[codigo_curso] = MatrizDispersa()

    # Cargar cada nota
    for actividad in root.find('notas'):
        nombre_actividad = actividad.get('nombre')
        carnet = actividad.get('carnet')
        valor = int(actividad.text)
        notas[codigo_curso].insertar(nombre_actividad, carnet, valor)

    return jsonify({'mensaje': 'Notas cargadas correctamente'})

@app.route('/notas/<codigo_curso>/<carnet>', methods=['GET'])
def obtener_notas(codigo_curso, carnet):
    if codigo_curso not in notas:
        return jsonify({'mensaje': 'Curso no encontrado'}), 404

    matriz = notas[codigo_curso]
    resultado = []

    for nodo in matriz.nodos:
        if nodo.columna == carnet:
            resultado.append({
                'actividad': nodo.fila,
                'nota': nodo.valor
            })

    return jsonify({'notas': resultado})

@app.route('/usuarios', methods=['GET'])
def ver_usuarios():
    return jsonify({'usuarios': usuarios})

@app.route('/horarios', methods=['POST'])
def cargar_horarios():
    archivo = request.data.decode('utf-8')
    
    try:
        root = ET.fromstring(archivo)
    except:
        return jsonify({'mensaje': 'XML inválido'}), 400

    horarios_cargados = []

    for curso in root.findall('curso'):
        codigo = curso.get('codigo')
        texto = curso.text

        # Extraer horario con expresión regular
        patron = r'HorarioI:\s*(\d{2}:\d{2})\s*HorarioF:\s*(\d{2}:\d{2})'
        resultado = re.search(patron, texto)

        if resultado:
            horario_inicio = resultado.group(1)
            horario_fin = resultado.group(2)
            horarios_cargados.append({
                'codigo': codigo,
                'inicio': horario_inicio,
                'fin': horario_fin
            })

    return jsonify({'horarios': horarios_cargados})

if __name__ == '__main__':
    app.run(debug=True, port=5000)