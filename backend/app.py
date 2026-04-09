from flask import Flask, request, jsonify

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)