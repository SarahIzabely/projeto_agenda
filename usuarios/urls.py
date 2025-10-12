from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('horarios/', views.listar_horarios, name='listar_horarios'),
    path('horarios/criar/', views.criar_horario, name='criar_horario'),
    path('horarios/editar/<int:pk>/', views.editar_horario, name='editar_horario'),
    path('horarios/deletar/<int:pk>/', views.deletar_horario, name='deletar_horario'),
    path('profissionais/', views.listar_profissionais, name='listar_profissionais'),
    path('profissional/<int:pk>/', views.detalhe_profissional, name='detalhe_profissional'),
]