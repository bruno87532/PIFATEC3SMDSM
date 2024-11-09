from django.shortcuts import render
from empresa.models import Doacao, Empresa
from django.views import View
from django.core.paginator import Paginator

class EmpresaDoacaoLista(View):
    def get(self, request, numero_pagina):
        doacoes = Doacao.objects.values('id_empresa', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto')
        lista_contexto = []
        empresas = {empresa.id: empresa.nome for empresa in Empresa.objects.all()}

        for i in list(doacoes):
            doacao = {
                'nome_empresa': empresas.get(int(i['id_empresa'])),
                'nome_produto': i['nome_produto'],
                'quantidade_produto': i['quantidade_produto'],
                'unidade_medida_produto': i['unidade_medida_produto'],
                'data_doado_produto': i['data_doado_produto'],
                'disponivel_produto': i['disponivel_produto']
            }
            lista_contexto.append(doacao)
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        if request.session.get('id_empresa') or request.session.get('id_pessoa'):
            return render(request=request, template_name='visualiza_doacao.html', context={'doacoes': pagina, 'logout': True})
        return render(request=request, template_name='visualiza_doacao.html', context={'doacoes': pagina})