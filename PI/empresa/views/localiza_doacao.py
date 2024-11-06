from django.shortcuts import render, redirect
from empresa.models import Doacao, Empresa
from django.views import View
from django.core.paginator import Paginator

class EmpresaDoacaoLocaliza(View):
    def obter_doacoes(self, nome_empresa):
        empresas = {empresa.id: empresa.nome_empresa for empresa in Empresa.objects.all()}
        lista_empresas = [i for i, e in empresas.items() if e == nome_empresa]
        lista_doacoes = list(Doacao.objects.filter(id_empresa__in=lista_empresas).values('id_empresa', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto'))
        return empresas, lista_doacoes
    def criar_contexto_doacoes(self, empresas, lista_doacoes):
        lista_contexto = [
            {
                'nome_empresa': empresas.get(int(i['id_empresa'])),
                'nome_produto': i['nome_produto'],
                'quantidade_produto': i['quantidade_produto'],
                'unidade_medida_produto': i['unidade_medida_produto'],
                'data_doado_produto': i['data_doado_produto'],
                'disponivel_produto': i['disponivel_produto'],
            }
            for i in lista_doacoes
        ]
        return lista_contexto
    def get(self, request, numero_pagina):
        if 'nome_empresa' in request.session:
            nome_empresa = request.session['nome_empresa']
            empresas, lista_doacoes = self.obter_doacoes(nome_empresa) 
            if not lista_doacoes:
                return render(request, 'visualiza_doacao_empresa.html', {'erro': 'erro', 'nome_empresa': nome_empresa})       
            lista_contexto = self.criar_contexto_doacoes(empresas, lista_doacoes)
            doacao_paginada = Paginator(lista_contexto, 10)
            pagina = doacao_paginada.get_page(numero_pagina)
            return render(request, 'visualiza_doacao_empresa.html', {'doacoes': pagina})       
        return redirect('empresa_doacao_list', numero_pagina=1)
    def post(self, request, numero_pagina):
        nome_empresa = request.POST.get('nome_empresa')
        request.session['nome_empresa'] = nome_empresa
        empresas, lista_doacoes = self.obter_doacoes(nome_empresa)   
        if not lista_doacoes:
            return render(request, 'visualiza_doacao_empresa.html', {'erro': 'erro', 'nome_empresa': nome_empresa})     
        lista_contexto = self.criar_contexto_doacoes(empresas, lista_doacoes)
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request, 'visualiza_doacao_empresa.html', {'doacoes': pagina})