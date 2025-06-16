# C:\Users\Eusse\AppData\Local\Programs\DjangoP\sprint8\djangovet\vet_sprint\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servicios/', views.services, name='services'), # El nombre de la URL sigue siendo 'services'
    path('contenido-dinamico/', views.dynamic_content_placeholder, name='dynamic_placeholder'), # El nombre de la URL sigue siendo 'dynamic_placeholder'
]