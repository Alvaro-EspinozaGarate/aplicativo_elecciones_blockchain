from django.db import models
from django.contrib.auth.models import User

class Candidato(models.Model):
    nombre = models.CharField(max_length=100)
    partido = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Voto(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} votó por {self.candidato.nombre}"
