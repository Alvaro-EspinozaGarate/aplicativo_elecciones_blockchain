import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votaciones.settings")
django.setup()

from usuarios.models import Candidato, Voto

print("Eliminando votos...")
Voto.objects.all().delete()

print("Eliminando candidatos...")
Candidato.objects.all().delete()

# Lista de candidatos iniciales
candidatos = [
    {"nombre": "Josue Julca Zeña", "partido": "Innovación UNFV", "cargo": "rector"},
    {"nombre": "Shirley Martinez Vargas", "partido": "Gestión Transparente", "cargo": "rector"},
    {"nombre": "Jordan Valenzuela Galvan", "partido": "Innovación UNFV", "cargo": "vicerrector"},
    {"nombre": "Alvaro Espinoza Garate", "partido": "Gestión Transparente", "cargo": "vicerrector"},
]

print("Creando nuevos candidatos...")
for c in candidatos:
    Candidato.objects.create(
        nombre=c["nombre"],
        partido=c["partido"],
        cargo=c["cargo"]
    )

print("✔ Candidatos reseteados y recreados correctamente.")
