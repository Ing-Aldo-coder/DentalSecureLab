from django.urls import path
from . import views


urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('nueva/', views.appointment_create, name='appointment_create'),
    path(
        '<int:pk>/editar/',
        views.appointment_update,
        name='appointment_update'
    ),
]