from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.payment_list,
        name='payment_list'
    ),

    path(
        'nuevo/',
        views.payment_create,
        name='payment_create'
    ),

    path(
        '<int:pk>/editar/',
        views.payment_update,
        name='payment_update'
    ),
]