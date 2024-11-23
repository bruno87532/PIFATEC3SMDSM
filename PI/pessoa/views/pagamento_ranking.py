from django.shortcuts import render
from pessoa.models import Pessoa
from django.views import View
    
class PessoaPagamentoRanking(View):
    def get(self, request, numero_pagina):
        pessoas = Pessoa.objects.all().order_by('-valor_total_doado_pessoa')[:10]
        lista_contexto = [
            {
                'nome_pessoa': i.nome_pessoa,
                'valor_total_doado_pessoa': i.valor_total_doado_pessoa
            } for i in pessoas
        ]
        return render(request=request, template_name='ranking_pagamento.html', context={'pessoas': lista_contexto})