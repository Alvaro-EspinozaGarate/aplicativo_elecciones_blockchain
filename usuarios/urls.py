from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('votar/', views.votar_view, name='votar'),
    path('resultados/', views.resultados_view, name='resultados'),
    path('voto_realizado/', views.voto_realizado_view, name='voto_realizado'),
    path('panel/', views.panel_view, name='panel'),

]
