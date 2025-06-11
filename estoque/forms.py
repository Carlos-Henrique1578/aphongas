from django import forms
from django.contrib.auth.models import User
from .models import Produto, Deposito, Fornecedor, Movimentacao

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = '__all__'

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff']

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'tipo', 'nome_cliente', 'fornecedor', 'deposito']