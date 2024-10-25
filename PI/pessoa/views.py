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
            pessoa = form.save(commit=False)
            pessoa.set_senha(form.cleaned_data['senha_login_pessoa'])
            pessoa.save()
            return redirect('login')
        else:
            lista_erro = list(form.errors.keys())
            lista_contexto = []
            if 'nome_pessoa' in lista_erro:
                nome_pessoa = {'nome_erro': 'Nome inválido'}
                lista_contexto.append(nome_pessoa)
            if 'cpf_pessoa' in lista_erro:
                erro = 0
                for n in form.errors.values():
                    if 'CPF já cadastrado' == n[0]:
                        erro = 1
                        cpf_existe = {'cpf_existe': 'CPF já cadastrado'}
                        lista_contexto.append(cpf_existe)
                        break
                if not erro:
                    cpf_erro = {'cpf_erro': 'CPF inválido'}
                    lista_contexto.append(cpf_erro)
            if 'email_login_pessoa' in lista_erro:
                email_erro = {'email_erro': 'Email já cadastro'}
                lista_contexto.append(email_erro)
            if 'senha_login_pessoa' in lista_erro:
                senha_erro = {'senha_erro': 'A senha deve possuir mais que 8 caracteres'}
                lista_contexto.append(senha_erro)
            if 'data_nascimento_pessoa' in lista_erro:
                data_nascimento_erro = {'data_nascimento_erro': 'Você deve ser maior que 18 anos'}
                lista_contexto.append(data_nascimento_erro)
            if 'telefone_pessoa' in lista_erro:
                telefone_pessoa = {'telefone_erro': 'Número de telefone inválido'}
                lista_contexto.append(telefone_pessoa)
            return render(request=request, template_name='cadastro.html', context={'form': form, 'erro': lista_contexto})
