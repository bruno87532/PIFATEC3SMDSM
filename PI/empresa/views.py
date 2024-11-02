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
            if not 'etapa1' in request.session:
                return redirect('empresagetcad', etapa = 1)
            template = 'cadastro_dois.html'
            form = EmpresaFormDois()
        elif etapa == 3:
            if not 'etapa2' in request.session:
                return redirect('empresagetcad', etapa = 1)
            template = 'cadastro_tres.html'
            form = EmpresaFormTres()
        return render(request=request, template_name=template, context={'form': form}) 
    def post(self, request):
        if request.POST.get('etapa1', ''):
            form = EmpresaFormUm(request.POST)
            if form.is_valid():
                request.session['empresa'] = form.cleaned_data
                request.session.modified = True
                request.session['etapa1'] = True
                return redirect('empresagetcad', etapa = 2)
            else:
                lista_erro = list(form.errors.keys())
                lista_contexto = []
                if 'cnpj_empresa' in lista_erro:
                    erro = 0
                    for n in form.errors.values():
                        print(form.errors.values())
                        if 'CNPJ já cadastrado' == n[0]:
                            erro = 1
                            cnpj_existe = {'cnpj_existe': 'CNPJ já cadastrado'}
                            lista_contexto.append(cnpj_existe)
                            break
                    if not erro:
                        cnpj_erro = {'cnpj_erro': 'CNPJ inválido'}
                        lista_contexto.append(cnpj_erro)
                if 'email_login_empresa' in lista_erro:
                    email_login_empresa = {'email_login_erro': 'Email já cadastrado'}
                    lista_contexto.append(email_login_empresa)
                if 'senha_login_empresa' in lista_erro:
                    senha_login_empresa = {'senha_login_erro': 'Senha inválida'}
                    lista_contexto.append(senha_login_empresa)
                return render(request=request, template_name='cadastro_um.html', context={'form': form, 'erro': lista_contexto})
            
        elif request.POST.get('etapa2', ''):
            form = EmpresaFormDois(request.POST)
            if form.is_valid():
                request.session['empresa'] = request.session['empresa'] | form.cleaned_data
                request.session.modified = True
                request.session['etapa2'] = True
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
                form_completo = EmpresaCompleta(request.session['empresa'])
                empresa = form_completo.save(commit=False)
                empresa.set_senha(form_completo.cleaned_data['senha_login_empresa'])
                empresa.save()
                return redirect('login')
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
            
class EmpresaDoacao(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_empresa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        return render(request=request, template_name='doacao_empresa.html')