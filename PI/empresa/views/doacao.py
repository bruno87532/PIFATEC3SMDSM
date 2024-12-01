from django.shortcuts import render, redirect
from empresa.forms import EmpresaDoacao as EmpresaDoacaoForm
from empresa.models import Empresa
from services.gerador_pdf import monta_pdf
from django.views import View

class EmpresaDoacao(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_empresa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        form = EmpresaDoacaoForm()
        return render(request=request, template_name='doacao_empresa.html', context={'form': form, 'logout': 'empresa'})
    def post(self, request):
        form = EmpresaDoacaoForm(request.POST)
        if form.is_valid():
            doacao = form.save(commit=False)
            doacao.id_empresa = request.session['id_empresa']
            empresa = Empresa.objects.get(id=request.session['id_empresa'])
            doacao.save()
            resposta = monta_pdf(doacao, empresa) 
            return resposta
        else:
            return render(request=request, template_name='doacao_empresa.html', context={'form': form, 'logout': 'empresa'}, status=400)