from django.shortcuts import render, redirect
from empresa.forms import EmpresaFormUm, EmpresaFormDois, EmpresaFormTres, EmpresaCompleta, EmpresaDoacao as EmpresaDoacaoForm
from empresa.models import Doacao, Empresa
from empresa.gerador_pdf import monta_pdf
from django.views import View
from django.core.paginator import Paginator

class GeraPdfView(View):
    def get(self, request, id):
        doacao = Doacao.objects.get(id=id)
        empresa = Empresa.objects.get(id=request.session['id_empresa'])
        resposta = monta_pdf(empresa.nome_empresa, empresa.cnpj_empresa, doacao.categoria_produto, doacao.data_doado_produto, doacao.nome_produto, doacao.descricao_produto, doacao.quantidade_produto, empresa.nome_representante_empresa, empresa.cpf_representante_empresa) 
        return resposta
