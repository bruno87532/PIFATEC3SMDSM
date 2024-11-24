from django.shortcuts import render, redirect
from empresa.models import Doacao, Empresa
from django.views import View
from django.core.paginator import Paginator
from services.contexto import GeraContexto

class EmpresaDoacaoLocaliza(View):
    def obter_doacoes(self, nome_empresa):
        empresas = {empresa.id: empresa.nome for empresa in Empresa.objects.all()}
        lista_empresas = [i for i, e in empresas.items() if e == nome_empresa]
        doacoes = list(Doacao.objects.filter(id_empresa__in=lista_empresas).values('id', 'id_empresa', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto'))
        return empresas, doacoes
    def get(self, request, numero_pagina):
        if 'nome_empresa' in request.session:
            nome_empresa = request.session['nome_empresa']
            empresas, doacoes = self.obter_doacoes(nome_empresa) 
            if not doacoes:
                return render(request, 'visualiza_doacao_empresa.html', {'erro': 'erro', 'nome_empresa': nome_empresa})       
            lista_contexto = GeraContexto.ContextoEmpresa(doacoes, empresas)
            doacao_paginada = Paginator(lista_contexto, 10)
            pagina = doacao_paginada.get_page(numero_pagina)
            return render(request, 'visualiza_doacao_empresa.html', {'doacoes': pagina})
        return redirect('empresa_doacao_lista', numero_pagina=1)
    def post(self, request, numero_pagina):
        nome_empresa = request.POST.get('nome_empresa')
        request.session['nome_empresa'] = nome_empresa
        empresas, doacoes = self.obter_doacoes(nome_empresa)   
        if not doacoes:
            return render(request, 'visualiza_doacao_empresa.html', {'erro': 'erro', 'nome_empresa': nome_empresa})     
        lista_contexto = GeraContexto.ContextoEmpresa(doacoes, empresas)
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request, 'visualiza_doacao_empresa.html', {'doacoes': pagina})