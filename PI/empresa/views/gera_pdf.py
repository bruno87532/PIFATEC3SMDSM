from django.shortcuts import render, redirect
from empresa.forms import EmpresaFormUm, EmpresaFormDois, EmpresaFormTres, EmpresaCompleta, EmpresaDoacao as EmpresaDoacaoForm
from empresa.models import Doacao, Empresa
from services.gerador_pdf import monta_pdf
from django.views import View
from django.core.paginator import Paginator

class GeraPdfView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_empresa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, id):
        doacao = Doacao.objects.get(id=id)
        empresa = Empresa.objects.get(id=request.session['id_empresa'])
        resposta = monta_pdf(doacao, empresa) 
        return resposta
