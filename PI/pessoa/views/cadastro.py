from django.shortcuts import render, redirect
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
            erros_chave = ['nome_erro', 'cpf_existe', 'cpf_erro', 'email_erro', 'senha_erro', 'telefone_erro', 'data_nascimento_erro']
            erros_valor = ['Nome inválido', 'CPF já cadastrado', 'CPF inválido', 'Email já cadastrado', 'Senha inválida', 'Número de telefone inválido', 'É necessário ser maior de idade']
            lista_erros = list(form.errors.values())
            lista_erros = [i for erro in lista_erros for i in erro]
            lista_contexto = []
            for c, v in zip(erros_chave, erros_valor):
                if v in lista_erros:
                    lista_contexto.append({c: v})
            return render(request=request, template_name='cadastro.html', context={'form': form, 'erro': lista_contexto})