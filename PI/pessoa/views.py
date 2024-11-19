from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from pessoa.forms import PessoaForm
from pessoa.forms import PessoaForm
from pessoa.models import Pessoa
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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

class PessoaDoacao(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_pessoa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        return render(request=request, template_name='pix.html')
    def post(self, request):
        site =  'http://localhost:8000'
        valor = int(request.POST['valor'])
        sessao_pagamento = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': f'Doacão de {valor} reais'
                        },
                        'unit_amount': valor * 100
                    },
                    'quantity': 1
                }
            ],
            mode = 'payment',
            success_url= site + '/pessoa/pagamento/sucessoredireciona?session_id={CHECKOUT_SESSION_ID}',
            cancel_url= site + '/pessoa/pagamento/cancelado',
        )
        return JsonResponse({'id': sessao_pagamento.id})
    
def rendeniza_sucesso(request):
    return render(request=request, template_name='success.html')

def redireciona_sucesso(request):
    session_id = request.GET.get('session_id')
    if session_id:
        valor = stripe.checkout.Session.retrieve(session_id).amount_total / 100
        pessoa = Pessoa.objects.get(id=request.session['id_pessoa'])
        pessoa.valor_total_doado_pessoa += valor
        pessoa.save()
    return redirect(reverse('pessoa_doacao_sucesso_rendeniza'))
def redireciona_cancelado(request):
    return render(request=request, template_name='cancel.html')