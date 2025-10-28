from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Voto

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel') 

            
            # 🔍 Verificar si el usuario ya votó
            if Voto.objects.filter(usuario=user).exists():
                return redirect('voto_realizado')  # Ya votó
            else:
                return redirect('votar')  # No ha votado
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'usuarios/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required
from .models import Candidato, Voto

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


from django.db.models import Count

@login_required
def resultados_view(request):
    resultados = Candidato.objects.annotate(total_votos=Count('voto')).order_by('-total_votos')
    return render(request, 'usuarios/resultados.html', {'resultados': resultados})


from django.contrib.auth.decorators import login_required
from .models import Voto

@login_required
def voto_realizado_view(request):
    voto = Voto.objects.filter(usuario=request.user).first()
    return render(request, 'usuarios/voto_realizado.html', {'voto': voto})


from django.contrib.auth.decorators import login_required
from .models import Voto

@login_required
def panel_view(request):
    voto = Voto.objects.filter(usuario=request.user).first()
    contexto = {
        'voto': voto
    }
    return render(request, 'usuarios/panel.html', contexto)
