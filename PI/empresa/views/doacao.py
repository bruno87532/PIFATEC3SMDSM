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
        return render(request=request, template_name='doacao_empresa.html', context={'form': form})
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
            lista_erro = list(form.errors.keys())
            lista_contexto = []
            if 'quantidade_produto' in lista_erro:
                quantidade_produto = {'quantidade_produto_erro': 'Quantidade inválida'}
                lista_contexto.append(quantidade_produto)
            if '__all__' in lista_erro:
                unidade_decimal = {'unidade_decimal_erro': 'O valor deve ser inteiro para medidas unitária'}
                lista_contexto.append(unidade_decimal)
            return render(request=request, template_name='doacao_empresa.html', context={'form': form, 'erro': lista_contexto}, status=400)