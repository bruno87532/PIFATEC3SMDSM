from django.shortcuts import render, redirect
from empresa.forms import EmpresaFormUm, EmpresaFormDois, EmpresaFormTres, EmpresaCompleta, EmpresaDoacao as EmpresaDoacaoForm
from empresa.models import Doacao, Empresa
from empresa.gerador_pdf import monta_pdf
from django.views import View
from django.core.paginator import Paginator

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
        form = EmpresaDoacaoForm()
        return render(request=request, template_name='doacao_empresa.html', context={'form': form})
    def post(self, request):
        form = EmpresaDoacaoForm(request.POST)
        if form.is_valid():
            doacao = form.save(commit=False)
            doacao.id_empresa = request.session['id_empresa']
            empresa = Empresa.objects.get(id=request.session['id_empresa'])
            doacao.save()
            monta_pdf(empresa.nome_empresa, empresa.cnpj_empresa, doacao.categoria_produto, doacao.data_doado_produto, doacao.data_doado_produto, doacao.nome_produto, doacao.descricao_produto, doacao.quantidade_produto, empresa.nome_representante_empresa, empresa.cpf_representante_empresa) 
            return redirect('home')
        else:
            lista_erro = list(form.errors.keys())
            lista_contexto = []
            if 'quantidade_produto' in lista_erro:
                quantidade_produto = {'quantidade_produto_erro': 'Quantidade inválida'}
                lista_contexto.append(quantidade_produto)
            if '__all__' in lista_erro:
                unidade_decimal = {'unidade_decimal_erro': 'O valor deve ser inteiro para medidas unitária'}
                lista_contexto.append(unidade_decimal)
            return render(request=request, template_name='doacao_empresa.html', context={'form': form, 'erro': lista_contexto})
        
class EmpresaDoacaoLista(View):
    def get(self, request, numero_pagina):
        doacoes = Doacao.objects.values('id_empresa', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto')
        lista_contexto = []
        
        empresas = {empresa.id: empresa.nome_empresa for empresa in Empresa.objects.all()}

        for i in list(doacoes):
            doacao = {
                'nome_empresa': empresas.get(i['id_empresa']),
                'nome_produto': i['nome_produto'],
                'quantidade_produto': i['quantidade_produto'],
                'unidade_medida_produto': i['unidade_medida_produto'],
                'data_doado_produto': i['data_doado_produto'],
                'disponivel_produto': i['disponivel_produto']
            }
            lista_contexto.append(doacao)
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request=request, template_name='visualiza_doacao.html', context={'doacoes': pagina})
