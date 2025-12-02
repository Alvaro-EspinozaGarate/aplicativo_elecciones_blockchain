import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votaciones.settings")
django.setup()

from usuarios.models import Candidato

# Lista de candidatos iniciales
candidatos = [
    {"nombre": "Juan Pérez", "partido": "Partido A", "cargo": "rector"},
    {"nombre": "María López", "partido": "Partido B", "cargo": "rector"},
    {"nombre": "Carlos Ramírez", "partido": "Partido C", "cargo": "vicerrector"},
    {"nombre": "Ana Torres", "partido": "Partido D", "cargo": "vicerrector"},
]

# BORRAR todo antes
print("Eliminando candidatos anteriores...")
Candidato.objects.all().delete()

# Crear nuevamente
print("Creando candidatos iniciales...")
for c in candidatos:
    Candidato.objects.create(
        nombre=c["nombre"],
        partido=c["partido"],
        cargo=c["cargo"]
    )

print("Candidatos recreados correctamente.")
