from django.shortcuts import render

# Create your views here.
# vet_app/views.py


def home(request):
    """
    Página de bienvenida
    """
    return render(request, 'vet_sprint/home.html', {'nombre_clinica': 'Clínica Veterinaria Amigos Peludos'})

def services(request):
    """
    Página de servicios
    """
    context = {
        'titulo': 'Nuestros Servicios Veterinarios',
        'servicios_list': [
            'Consultas generales y vacunación',
            'Registros de usuarios y mascotas',
            'Manejo de información de personas y mascotas',
            'Eliminación de usuarios',
         
        ],
        'descripcion_adicional': 'Ofrecemos el mejor cuidado para tus mascotas.'
    }
    return render(request, 'vet_sprint/service.html', context)

def dynamic_content_placeholder(request):
    """
    Página con placeholders
    """
    context = {
        'page_title': 'Información',
        'sections': {
            'mascotas': 'Aquí se mostrarán las mascotas registradas.',
            'citas': 'Aquí se listarán las citas programadas.',
            'duenos': 'Aquí se presentará la información de los dueños.'
        }
    }
    return render(request, 'vet_sprint/info.html', context)