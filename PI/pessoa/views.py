from django.shortcuts import render, redirect
from pessoa.forms import PessoaForm
from pessoa.forms import PessoaForm
from django.views import View

# Create your views here.

class PessoaCadastro(View):
    def get(self, request):
        form = PessoaForm()
        return render(request=request, template_name='cadastro.html',  context={'form': form})
    def post(self, request):
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pessoalogin')
        else:
            lista_erro = list(form.errors.keys())
            lista_contexto = []
            if 'nome_pessoa' in lista_erro:
                nome_pessoa = {'nome_erro': 'Nome inválido'}
                lista_contexto.append(nome_pessoa)
            if 'cpf_pessoa' in lista_erro:
                cpf_erro = {'cpf_erro': 'CPF inválido'}
                lista_contexto.append(cpf_erro)
            if 'data_nascimento_pessoa' in lista_erro:
                data_nascimento_erro = {'data_nascimento_erro': 'Data de nascimento inválida'}
                lista_contexto.append(data_nascimento_erro)
            if 'telefone_pessoa' in lista_erro:
                telefone_pessoa = {'telefone_erro': 'Número de telefone inválido'}
                lista_contexto.append(telefone_pessoa)
            return render(request=request, template_name='cadastro.html', context={'form': form, 'erro': lista_contexto})

class PessoaLogin(View):
    def get(self, request):
        return render(request=request, template_name='login.html')