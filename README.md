# PPCYL2-AcadNet
Proyecto 2 - Programación para la Ciencia y la Ingeniería II
Universidad Mariano Galvez de Guatemala

## Descripción
PPCYL2-AcadNet es una plataforma web educativa que conecta estudiantes con tutores. 
Permite gestionar sesiones de tutoría, cargar notas y generar reportes académicos.

## Arquitectura
El sistema usa arquitectura cliente-servidor con dos servicios:
- **Frontend**: Django (puerto 8000)
- **Backend**: Flask API (puerto 5000)

## Cómo ejecutar el proyecto

### Backend (Flask)
```bash
cd backend
python app.py
```

### Frontend (Django)
```bash
cd frontend
python manage.py runserver
```

## Endpoints de la API

| Endpoint | Método | Descripción |
|---|---|---|
| `/login` | POST | Iniciar sesión |
| `/cargar` | POST | Cargar XML de configuración |
| `/usuarios` | GET | Ver todos los usuarios |
| `/notas` | POST | Cargar notas |
| `/notas/<curso>/<carnet>` | GET | Consultar notas de un estudiante |
| `/horarios` | POST | Cargar horarios |
| `/reporte/promedio/<curso>` | GET | Reporte de promedios por actividad |

## Usuarios por defecto
- **Administrador**: AdminPPCYL2 / AdminPPCYL2771

## Tecnologías utilizadas
- Python 3.9
- Flask
- Django
- ChartJS
- XML
- Expresiones Regulares
- Matriz Dispersa (POO)