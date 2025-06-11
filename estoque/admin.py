from django.contrib import admin
from .models import Deposito, Fornecedor, Produto

admin.site.register(Deposito)
admin.site.register(Fornecedor)
admin.site.register(Produto)
