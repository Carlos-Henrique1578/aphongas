from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Produto, Deposito, Fornecedor, Movimentacao
from .forms import ProdutoForm, DepositoForm, FornecedorForm, UsuarioForm, MovimentacaoForm

def home(request):
    return render(request, 'home.html')

@login_required
def produtos(request):
    produtos = Produto.objects.all()
    form = ProdutoForm()
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos')
    return render(request, 'produtos.html', {'form': form, 'produtos': produtos})

@login_required
def depositos(request):
    todos = Deposito.objects.all()
    form = DepositoForm()
    if request.method == 'POST':
        form = DepositoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('depositos')
    return render(request, 'depositos.html', {'form': form, 'depositos': todos})

@login_required
def fornecedores(request):
    todos = Fornecedor.objects.all()
    form = FornecedorForm()
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    return render(request, 'fornecedores.html', {'form': form, 'fornecedores': todos})

@login_required
@user_passes_test(lambda u: u.is_staff)
def usuarios(request):
    todos = User.objects.all()
    form = UsuarioForm()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('usuarios')
    return render(request, 'usuarios.html', {'form': form, 'usuarios': todos})

@login_required
def movimentacoes(request):
    todos = Movimentacao.objects.all().order_by('-dthr_movimentacao')
    form = MovimentacaoForm()
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            mov.usuario = request.user
            if mov.tipo == 'S':
                entradas = Movimentacao.objects.filter(produto=mov.produto, tipo='E').aggregate(Sum('quantidade'))['quantidade__sum'] or 0
                saidas = Movimentacao.objects.filter(produto=mov.produto, tipo='S').aggregate(Sum('quantidade'))['quantidade__sum'] or 0
                saldo = entradas - saidas
                if mov.quantidade > saldo:
                    messages.error(request, f'Estoque insuficiente! Saldo atual: {saldo}')
                    return redirect('movimentacoes')
            mov.save()
            messages.success(request, 'Movimentação registrada com sucesso.')
            return redirect('movimentacoes')
    return render(request, 'movimentacoes.html', {'form': form, 'movimentacoes': todos})

@login_required
def relatorio(request):
    produtos = Produto.objects.all()
    dados = []

    for produto in produtos:
        entradas = Movimentacao.objects.filter(produto=produto, tipo='E').aggregate(Sum('quantidade'))['quantidade__sum'] or 0
        saidas = Movimentacao.objects.filter(produto=produto, tipo='S').aggregate(Sum('quantidade'))['quantidade__sum'] or 0
        saldo = entradas - saidas
        dados.append({
            'produto': produto,
            'entradas': entradas,
            'saidas': saidas,
            'saldo': saldo,
        })

    return render(request, 'relatorio.html', {'dados': dados})
