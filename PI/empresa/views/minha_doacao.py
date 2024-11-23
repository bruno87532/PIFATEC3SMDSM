from django.shortcuts import render, redirect
from empresa.models import Doacao, Empresa
from django.views import View
from django.core.paginator import Paginator
from datetime import timedelta
from services.contexto import GeraContexto

class EmpresaDoacaoMinha(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_empresa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, numero_pagina):
        doacoes = Doacao.objects.filter(id_empresa=request.session['id_empresa']).values('id', 'id_empresa', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto')
        empresas = Empresa.objects.get(id=request.session['id_empresa'])
        lista_contexto = GeraContexto.ContextoEmpresa(doacoes, empresas)
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request, 'visualiza_doacao_minha.html', {'doacoes': pagina})