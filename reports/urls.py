from django.urls import path
from . import views

urlpatterns = [
    path('empleado/', views.empleado_dashboard, name='empleado_dashboard'),
    path('create/', views.create_report, name='create_report'),
    path('contador/', views.contador_dashboard, name='contador_dashboard'),
    path('empleado/<int:empleado_id>/performance/', views.empleado_performance, name='empleado_performance'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
]
