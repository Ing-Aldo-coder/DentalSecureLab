from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('nuevo/', views.patient_create, name='patient_create'),

    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:pk>/editar/', views.patient_update, name='patient_update'),
    path('<int:pk>/eliminar/', views.patient_delete, name='patient_delete'),
]