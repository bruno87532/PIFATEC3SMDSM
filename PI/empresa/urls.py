from django.urls import path
from empresa.views import EmpresaCadastro, EmpresaDoacao
urlpatternscad = [
    path('', EmpresaCadastro.as_view(), name='empresapostcad'),
    path('<int:etapa>/', EmpresaCadastro.as_view(), name='empresagetcad')
]
urlpatternsdoacao = [
    path('', EmpresaDoacao.as_view(), name='empresa_doacao')
]