from django.db import models
from django.contrib.auth.models import User


# Depósito
class Deposito(models.Model):
    descricao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.descricao


# Fornecedor
class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Produto
class Produto(models.Model):
    UNIDADES = [
        ('ml', 'Mililitro'),
        ('lt', 'Litro'),
        ('g', 'Grama'),
        ('kg', 'Quilograma'),
        ('m3', 'Metro cúbico'),
    ]

    descricao = models.CharField(max_length=100)
    unidade = models.CharField(max_length=10, choices=UNIDADES)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    deposito_padrao = models.ForeignKey(Deposito, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao


# Movimentação de produtos
class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    nome_cliente = models.CharField(max_length=100, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dthr_movimentacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.produto} ({self.quantidade})'
