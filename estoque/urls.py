from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('depositos/', views.depositos, name='depositos'),
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),
    path('relatorio/', views.relatorio, name='relatorio'),
]
