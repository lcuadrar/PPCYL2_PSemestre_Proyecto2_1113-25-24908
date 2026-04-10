from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
app = Flask(__name__)

# Aquí guardaremos todos los datos en memoria
usuarios = []
cursos = []
tutores = []
estudiantes = []

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)