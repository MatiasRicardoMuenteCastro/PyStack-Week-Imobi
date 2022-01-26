from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = "home"),
    path('imovel/<str:id>',views.imovel, name = "imovel"),
    path('agendar_visitas/',views.agendarVisitas, name = "agendar_visitas"),
    path('agendamentos/',views.agendamentos, name = "agendamentos" ),
    path('cancelar_agendamento/<str:id>',views.cancelarAgendamento, name = "cancelar_agendamento")
]