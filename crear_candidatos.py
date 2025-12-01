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

# Crear candidatos si no existen
for c in candidatos:
    Candidato.objects.get_or_create(nombre=c["nombre"], cargo=c["cargo"], defaults={"partido": c["partido"]})

print("Candidatos iniciales creados o ya existentes.")