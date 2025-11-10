from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from agenda import views as agenda_views
from usuarios import views as usuarios_views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', agenda_views.home, name='home'),

    # Horários agenda
    path('horarios/', agenda_views.listar_horarios, name='listar_horarios'),
    path('horarios/criar/', agenda_views.criar_horario, name='criar_horario'),
    path('horarios/editar/<int:pk>/', agenda_views.editar_horario, name='editar_horario'),
    path('horarios/deletar/<int:pk>/', agenda_views.deletar_horario, name='deletar_horario'),
    path('horarios/<int:pk>/', usuarios_views.detalhes_consulta, name='detalhes_consulta'),
    path('confirmar_agendamento/<int:pk>/', usuarios_views.confirmar_agendamento, name='confirmar_agendamento'),
    path('horarios/agendados/', usuarios_views.horarios_agendados, name='horarios_agendados'),


    # 🔍 Debug (ver todos os horários no banco)
    path('debug/horarios/', agenda_views.ver_horarios_debug, name='ver_horarios_debug'),

    # Usuários
    path('usuarios/', include('usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
