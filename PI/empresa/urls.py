from django.urls import path
from empresa.views import EmpresaCadastro, EmpresaLogin
urlpatternscad = [
    path('', EmpresaCadastro.as_view(), name='empresapostcad'),
    path('<int:etapa>/', EmpresaCadastro.as_view(), name='empresagetcad')
]
urlpatternslogin = [
    path('', EmpresaLogin.as_view(), name='empresagetlogin')
]