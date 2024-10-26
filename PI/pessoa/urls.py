from django.urls import path
from pessoa.views import PessoaCadastro, PessoaDoacao
urlpatternscad = [
    path('', PessoaCadastro.as_view(), name='pessoa'),
]

urlpatternsdoacao = [
    path('', PessoaDoacao.as_view(), name='pessoa_doacao')
]