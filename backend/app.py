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
    usuarios.clear()

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

    # Contar asignaciones
    asignaciones_tutores_total = 0
    asignaciones_tutores_correctas = 0
    asignaciones_tutores_incorrectas = 0

    for tutor_curso in root.find('asignaciones').find('c_tutores'):
        asignaciones_tutores_total += 1
        codigo = tutor_curso.get('codigo')
        registro = tutor_curso.text
        curso_existe = any(c['codigo'] == codigo for c in cursos)
        tutor_existe = any(t['usuario'] == registro for t in tutores)
        if curso_existe and tutor_existe:
            asignaciones_tutores_correctas += 1
        else:
            asignaciones_tutores_incorrectas += 1

    asignaciones_estudiantes_total = 0
    asignaciones_estudiantes_correctas = 0
    asignaciones_estudiantes_incorrectas = 0

    for est_curso in root.find('asignaciones').find('c_estudiante'):
        asignaciones_estudiantes_total += 1
        codigo = est_curso.get('codigo')
        carnet = est_curso.text
        curso_existe = any(c['codigo'] == codigo for c in cursos)
        estudiante_existe = any(e['usuario'] == carnet for e in estudiantes)
        if curso_existe and estudiante_existe:
            asignaciones_estudiantes_correctas += 1
        else:
            asignaciones_estudiantes_incorrectas += 1

    # Generar XML de salida
    xml_salida = f"""<?xml version="1.0"?>
<configuraciones_aplicadas>
    <tutores_cargados>{len(tutores)}</tutores_cargados>
    <estudiantes_cargados>{len(estudiantes)}</estudiantes_cargados>
    <asignaciones>
        <tutores>
            <total>{asignaciones_tutores_total}</total>
            <correcto>{asignaciones_tutores_correctas}</correcto>
            <incorrecto>{asignaciones_tutores_incorrectas}</incorrecto>
        </tutores>
        <estudiantes>
            <total>{asignaciones_estudiantes_total}</total>
            <correcto>{asignaciones_estudiantes_correctas}</correcto>
            <incorrecto>{asignaciones_estudiantes_incorrectas}</incorrecto>
        </estudiantes>
    </asignaciones>
</configuraciones_aplicadas>"""

    return xml_salida, 200, {'Content-Type': 'text/xml'}

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

@app.route('/reporte/promedio/<codigo_curso>', methods=['GET'])
def reporte_promedio(codigo_curso):
    if codigo_curso not in notas:
        return jsonify({'mensaje': 'Curso no encontrado'}), 404

    matriz = notas[codigo_curso]
    
    # Agrupar notas por actividad
    actividades = {}
    for nodo in matriz.nodos:
        if nodo.fila not in actividades:
            actividades[nodo.fila] = []
        actividades[nodo.fila].append(nodo.valor)

    # Calcular promedio por actividad
    promedios = []
    for actividad, valores in actividades.items():
        promedio = sum(valores) / len(valores)
        promedios.append({
            'actividad': actividad,
            'promedio': round(promedio, 2)
        })

    return jsonify({'promedios': promedios})

@app.route('/cursos/<carnet>', methods=['GET'])
def cursos_estudiante(carnet):
    cursos_del_estudiante = []
    for asignacion in cursos:
        cursos_del_estudiante.append({
            'codigo': asignacion['codigo'],
            'nombre': asignacion['nombre']
        })
    return jsonify({'cursos': cursos_del_estudiante})

if __name__ == '__main__':
    app.run(debug=True, port=5000)