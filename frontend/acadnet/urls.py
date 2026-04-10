from django.urls import path
from main import views

urlpatterns = [
    path('', views.login, name='login'),
    path('inicio/', views.inicio, name='inicio'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('cargar_xml/', views.cargar_xml, name='cargar_xml'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('tutor_panel/', views.tutor_panel, name='tutor_panel'),
    path('cargar_horarios/', views.cargar_horarios, name='cargar_horarios'),
    path('cargar_notas/', views.cargar_notas, name='cargar_notas'),
    path('estudiante_panel/', views.estudiante_panel, name='estudiante_panel'),
    path('reporte_notas/', views.reporte_notas, name='reporte_notas'),
]