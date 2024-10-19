from django.urls import path
from pessoa.views import PessoaCadastro, PessoaLogin
urlpatternscad = [
    path('', PessoaCadastro.as_view(), name='pessoa'),
]
urlpatternslogin = [
    path('', PessoaLogin.as_view(), name='pessoalogin')
]
