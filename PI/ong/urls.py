from django.urls import path
from ong.views import OngCadastro

urlpatternscad = [
    path('', OngCadastro.as_view(), name='ongpostcad'),
    path('<int:etapa>/', OngCadastro.as_view(), name='onggetcad')
]