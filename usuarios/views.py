import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Voto, Candidato
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .blockchain import Blockchain

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def votar_view(request):
    usuario = request.user

    # Si ya votó, no permitir votar otra vez
    if Voto.objects.filter(usuario=usuario).exists():
        return redirect('voto_realizado')

    candidatos_rector = Candidato.objects.filter(cargo="rector")
    candidatos_vicerrector = Candidato.objects.filter(cargo="vicerrector")

    if request.method == "POST":
        rector_id = request.POST.get("rector")
        vicerrector_id = request.POST.get("vicerrector")

        if not rector_id or not vicerrector_id:
            messages.error(request, "Debe seleccionar ambos candidatos.")
            return redirect("votar")

        rector = Candidato.objects.get(id=rector_id)
        vicer = Candidato.objects.get(id=vicerrector_id)

        # Registrar voto en la BD
        voto = Voto.objects.create(
            usuario=usuario,
            rector=rector,
            vicerrector=vicer
        )

        # Registrar voto en la blockchain
        blockchain.add_vote(
            usuario.username,
            rector.nombre,
            vicer.nombre
        )

        # Crear nuevo bloque automáticamente
        blockchain.new_block(proof=100)

        # Guardar blockchain en archivo JSON
        with open('blockchain.json', 'w') as f:
            json.dump(blockchain.chain, f, indent=4)

        return redirect("voto_realizado")

    return render(request, "usuarios/votar.html", {
        "usuario": usuario,
        "candidatos_rector": candidatos_rector,
        "candidatos_vicerrector": candidatos_vicerrector,
    })




@login_required
def resultados_view(request):

    # Resultados para RECTOR
    resultados_rector = (
        Candidato.objects.filter(cargo="rector")
        .annotate(total_votos=Count("votos_rector"))
        .order_by("-total_votos")
    )

    # Resultados para VICERRECTOR
    resultados_vicerrector = (
        Candidato.objects.filter(cargo="vicerrector")
        .annotate(total_votos=Count("votos_vicerrector"))
        .order_by("-total_votos")
    )

    # Determinar ganadores y empates
    empatados_rector = []
    empatados_vicerrector = []

    if resultados_rector:
        max_votos_rector = resultados_rector[0].total_votos
        empatados_rector = [
            c for c in resultados_rector if c.total_votos == max_votos_rector
        ]

    if resultados_vicerrector:
        max_votos_vicer = resultados_vicerrector[0].total_votos
        empatados_vicerrector = [
            c for c in resultados_vicerrector if c.total_votos == max_votos_vicer
        ]

    return render(request, "usuarios/resultados.html", {
        "resultados_rector": resultados_rector,
        "resultados_vicerrector": resultados_vicerrector,
        "empatados_rector": empatados_rector,
        "empatados_vicerrector": empatados_vicerrector,
    })



@login_required
def voto_realizado_view(request):
    voto = Voto.objects.filter(usuario=request.user).first()
    return render(request, 'usuarios/voto_realizado.html', {'voto': voto})

@login_required
def panel_view(request):
    voto = Voto.objects.filter(usuario=request.user).first()
    return render(request, "usuarios/panel.html", {"voto": voto})


# Inicializa blockchain (podrías hacerlo global o singleton)
blockchain = Blockchain()


