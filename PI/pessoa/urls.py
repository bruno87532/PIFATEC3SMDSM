from django.urls import path
from pessoa.views import PessoaCadastro, PessoaDoacao, redireciona_sucesso, redireciona_cancelado, rendeniza_sucesso
urlpatternscad = [
    path('', PessoaCadastro.as_view(), name='pessoa'),
]

urlpatternsdoacao = [
    path('', PessoaDoacao.as_view(), name='pessoa_doacao'),
    path('sucessoredireciona', redireciona_sucesso, name='pessoa_doacao_sucesso'),
    path('sucesso', rendeniza_sucesso, name='pessoa_doacao_sucesso_rendeniza'),
    path('cancelado', redireciona_cancelado, name='pessoa_doacao_cancelado'),
]