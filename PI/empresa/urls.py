from django.urls import path
from empresa.views import EmpresaCadastro, EmpresaDoacao, EmpresaDoacaoLista
urlpatternscad = [
    path('', EmpresaCadastro.as_view(), name='empresapostcad'),
    path('<int:etapa>/', EmpresaCadastro.as_view(), name='empresagetcad')
]
urlpatternsdoacao = [
    path('', EmpresaDoacao.as_view(), name='empresa_doacao'),
    path('lista/<int:numero_pagina>/', EmpresaDoacaoLista.as_view(), name='empresa_doacao_lista')
]