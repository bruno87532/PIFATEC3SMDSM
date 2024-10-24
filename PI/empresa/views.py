from django.shortcuts import render, redirect
from empresa.forms import EmpresaFormUm, EmpresaFormDois, EmpresaFormTres, EmpresaCompleta
from django.views import View

# Create your views here.

class EmpresaCadastro(View):
    def get(self, request, etapa):
        if etapa == 1:
            template = 'cadastro_um.html'
            form = EmpresaFormUm()
        elif etapa == 2:
            template = 'cadastro_dois.html'
            form = EmpresaFormDois()
        elif etapa == 3:
            template = 'cadastro_tres.html'
            form = EmpresaFormTres()
        return render(request=request, template_name=template, context={'form': form}) 
    def post(self, request):
        if request.POST.get('etapa1', ''):
            form = EmpresaFormUm(request.POST)
            if form.is_valid():
                request.session['empresa'] = form.cleaned_data
                request.session.modified = True
                print(request.session['empresa'])
                return redirect('empresagetcad', etapa = 2)
            else:
                lista_erro = list(form.errors.keys())
                lista_contexto = []
                if 'cnpj_empresa' in lista_erro:
                    cnpj_empresa = {'cnpj_erro': 'CNPJ inválido'}
                    lista_contexto.append(cnpj_empresa)
                if 'senha_login_empresa' in lista_erro:
                    senha_login_empresa = {'senha_login_erro': 'Senha inválida'}
                    lista_contexto.append(senha_login_empresa)
                return render(request=request, template_name='cadastro_um.html', context={'form': form, 'erro': lista_contexto})
            
        elif request.POST.get('etapa2', ''):
            form = EmpresaFormDois(request.POST)
            if form.is_valid():
                request.session['empresa'] = request.session['empresa'] | form.cleaned_data
                request.session.modified = True
                print(request.session['empresa'])
                return redirect('empresagetcad', etapa = 3)
            else:
                lista_erro = list(form.errors.keys())
                lista_contexto = []
                if 'cep_empresa' in lista_erro:
                    cep_empresa = {'cep_erro': 'CEP inválido'}
                    lista_contexto.append(cep_empresa)
                return render(request=request, template_name='cadastro_dois.html', context={'form': form, 'erro': lista_contexto})
        elif request.POST.get('etapa3', ''):
            form = EmpresaFormTres(request.POST)
            if form.is_valid():
                request.session['empresa'] = request.session['empresa'] | form.cleaned_data
                print(request.session['empresa'])
                form_completo = EmpresaCompleta(request.session['empresa'])
                form_completo.save()
                return redirect('empresagetlogin')
            else:
                lista_erro = list(form.errors.keys())
                lista_contexto = []
                if 'nome_representante_empresa' in lista_erro:
                    nome_representante_empresa = {'nome_representante_erro': 'Nome inválido'}
                    lista_contexto.append(nome_representante_empresa)
                if 'cpf_representante_empresa' in lista_erro:
                    cpf_representante_empresa = {'cpf_representante_erro': 'CPF inválido'}
                    lista_contexto.append(cpf_representante_empresa)
                if 'telefone_representante_empresa':
                    telefone_representante_empresa = {'telefone_representante_erro': 'Telefone inválido'}
                    lista_contexto.append(telefone_representante_empresa)
                return render(request=request, template_name='cadastro_tres.html', context={'form': form, 'erro': lista_contexto})
            
class EmpresaLogin(View):
    def get(self, request):
        return render(request=request, template_name='login_empresa.html')