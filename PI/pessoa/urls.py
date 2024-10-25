from django.urls import path
from pessoa.views import PessoaCadastro
urlpatternscad = [
    path('', PessoaCadastro.as_view(), name='pessoa'),
]