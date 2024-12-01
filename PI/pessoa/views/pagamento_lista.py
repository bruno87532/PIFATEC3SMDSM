from django.shortcuts import render
from pessoa.models import Pessoa, Doacao
from django.views import View
from django.core.paginator import Paginator

class PessoaPagamentoLista(View):
    def get(self, request, numero_pagina):
        login = {
            'id_empresa': 'empresa',
            'id_ong': 'ong',
            'id_pessoa': 'pessoa'
        }
        for k, v in login.items():
            if request.session.get(k):
                context = v
                break
            context = ''
        pessoas = {i.id: i.nome_pessoa for i in Pessoa.objects.all()}
        doacoes = Doacao.objects.all()
        lista_contexto = [
            {
                'nome_pessoa': pessoas.get(int(i.id_pessoa)),
                'valor_doado': int(i.valor_doacao) if i.valor_doacao % 10 == 0 else i.valor_doacao,
                'data_doado': i.data_doado   
            } for i in doacoes
        ]
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request=request, template_name='visualiza_pagamento.html', context={'doacoes': pagina, 'logout': context})