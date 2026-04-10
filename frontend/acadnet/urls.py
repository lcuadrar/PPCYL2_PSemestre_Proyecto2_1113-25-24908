from django.urls import path
from main import views

urlpatterns = [
    path('', views.login, name='login'),
    path('inicio/', views.inicio, name='inicio'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('cargar_xml/', views.cargar_xml, name='cargar_xml'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
]