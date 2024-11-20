from django.shortcuts import render, redirect
from pessoa.models import Pessoa, Doacao
from django.views import View
from django.core.paginator import Paginator

class PessoaPagamentoProprio(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_pessoa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, numero_pagina):
        doacoes = Doacao.objects.filter(id_pessoa=request.session['id_pessoa'])
        pessoa = Pessoa.objects.get(id=request.session['id_pessoa']).nome_pessoa
        lista_contexto = [
            {
                'valor_doado': int(i.valor_doacao) if i.valor_doacao % 10 == 0 else i.valor_doacao,
                'data_doado': i.data_doado
            } for i in doacoes
        ]
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request=request, template_name='visualiza_pagamento_meu.html', context={'doacoes': pagina, 'nome': pessoa})