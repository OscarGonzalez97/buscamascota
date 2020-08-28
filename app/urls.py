from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colaborar/', views.colaborar, name='colaborar'),
    path('map/', views.map, name='map'),
]