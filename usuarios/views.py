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
    # Verificar si el usuario ya votó
    try:
        voto_existente = Voto.objects.get(usuario=request.user)
        return render(request, 'usuarios/voto_realizado.html', {'voto': voto_existente})
    except Voto.DoesNotExist:
        pass  # El usuario aún no ha votado

    # Si llega un voto por POST
    if request.method == 'POST':
        candidato_id = request.POST.get('candidato')
        candidato = Candidato.objects.get(id=candidato_id)
        Voto.objects.create(usuario=request.user, candidato=candidato)
        return render(request, 'usuarios/voto_realizado.html', {'voto': candidato})

    candidatos = Candidato.objects.all()
    return render(request, 'usuarios/votar.html', {'candidatos': candidatos})

@login_required
def resultados_view(request):
    resultados = (
        Candidato.objects
        .annotate(total_votos=Count('voto'))
        .order_by('-total_votos')
    )

    if not resultados:
        return render(request, 'usuarios/resultados.html', {
            'resultados': resultados,
            'empatados': [],
        })

    max_votos = resultados[0].total_votos

    # Lista de candidatos que están empatados en primer lugar
    empatados = [c for c in resultados if c.total_votos == max_votos]

    return render(request, 'usuarios/resultados.html', {
        'resultados': resultados,
        'empatados': empatados,
    })


@login_required
def voto_realizado_view(request):
    voto = Voto.objects.filter(usuario=request.user).first()
    return render(request, 'usuarios/voto_realizado.html', {'voto': voto})

@login_required
def panel_view(request):
    voto = Voto.objects.filter(usuario=request.user).first()
    contexto = {
        'voto': voto
    }
    return render(request, 'usuarios/panel.html', contexto)

# Inicializa blockchain (podrías hacerlo global o singleton)
blockchain = Blockchain()

@login_required
def votar_view(request):
    voto_existente = Voto.objects.filter(usuario=request.user).first()
    if voto_existente:
        return render(request, 'usuarios/voto_realizado.html', {'voto': voto_existente})

    if request.method == 'POST':
        candidato_id = request.POST.get('candidato')
        try:
            candidato = Candidato.objects.get(id=candidato_id)
            Voto.objects.create(usuario=request.user, candidato=candidato)

            # Registrar voto en blockchain local
            blockchain.new_transaction(usuario=request.user.username, candidato=candidato.nombre)
            last_block = blockchain.last_block
            blockchain.new_block(proof=12345)  # prueba simple

            # Opcional: guardar blockchain en archivo local (persistencia)
            with open('blockchain.json', 'w') as f:
                json.dump(blockchain.chain, f, indent=4)

            messages.success(request, f"Voto registrado y verificado en blockchain.")
            return render(request, 'usuarios/voto_realizado.html', {'voto': candidato})
        except Candidato.DoesNotExist:
            messages.error(request, "El candidato seleccionado no existe.")
            return redirect('votar')

    candidatos = Candidato.objects.all()
    return render(request, 'usuarios/votar.html', {'candidatos': candidatos})

