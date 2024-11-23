from django.shortcuts import render
from empresa.models import Doacao, Empresa
from django.views import View
from django.core.paginator import Paginator
from services.contexto import GeraContexto

class EmpresaDoacaoLista(View):
    def get(self, request, numero_pagina):
        doacoes = Doacao.objects.values('id', 'id_empresa', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto')
        empresas = {empresa.id: empresa.nome for empresa in Empresa.objects.all()}
        lista_contexto = GeraContexto.ContextoEmpresa(doacoes, empresas)
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        if request.session.get('id_empresa') or request.session.get('id_pessoa') or request.session.get('id_ong'):
            return render(request=request, template_name='visualiza_doacao.html', context={'doacoes': pagina, 'logout': True})
        return render(request=request, template_name='visualiza_doacao.html', context={'doacoes': pagina})