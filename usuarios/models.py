from django.db import models
from django.contrib.auth.models import User

class Candidato(models.Model):
    CARGOS = (
        ('rector', 'Rector'),
        ('vicerrector', 'Vicerrector'),
    )

    nombre = models.CharField(max_length=100)
    partido = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=20, choices=CARGOS)

    def __str__(self):
        return f"{self.nombre} ({self.get_cargo_display()})"


class Voto(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    rector = models.ForeignKey(
        Candidato, related_name="votos_rector",
        limit_choices_to={'cargo': 'rector'},
        on_delete=models.CASCADE, null=True, blank=True
    )

    vicerrector = models.ForeignKey(
        Candidato, related_name="votos_vicerrector",
        limit_choices_to={'cargo': 'vicerrector'},
        on_delete=models.CASCADE, null=True, blank=True
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        rector = self.rector.nombre if self.rector else "N/A"
        vicer = self.vicerrector.nombre if self.vicerrector else "N/A"
        return f"{self.usuario.username} votó por {rector} y {vicer}"
