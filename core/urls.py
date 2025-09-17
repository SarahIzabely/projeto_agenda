from django.contrib import admin
from django.urls import path
from agenda.views import cadastro_paciente, login_paciente, dashboard, profissionais_view, book_appointment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Tela inicial de login (raiz)
    path('', login_paciente, name='login_paciente'),

    # Cadastro de paciente
    path('paciente/cadastro/', cadastro_paciente, name='cadastro_paciente'),

    # Dashboard do paciente (após login/cadastro)
    path('paciente/dashboard/', dashboard, name='dashboard'),

    # Listagem de profissionais
    path('paciente/profissionais/', profissionais_view, name='profissionais'),

    # Agendamentos
    path('paciente/agendamento/book/', book_appointment, name='book_appointment'),
]

# Para servir imagens durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
