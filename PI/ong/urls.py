from django.urls import path
from ong.views import OngCadastro, OngDistribuicao

urlpatternscad = [
    path('', OngCadastro.as_view(), name='ongpostcad'),
    path('<int:etapa>/', OngCadastro.as_view(), name='onggetcad')
]

urlpatterns = [
    path('<int:numero_pagina>/', OngDistribuicao.as_view(), name='distribuicao_ong')
]