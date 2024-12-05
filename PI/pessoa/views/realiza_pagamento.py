from django.shortcuts import render, redirect
from pessoa.models import Pessoa, Doacao
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class PessoaDoacao(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_pessoa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        return render(request=request, template_name='pix.html', context={'logout': 'pessoa'})
    def post(self, request):
        site =  'http://127.0.0.1:8000/'
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
    return render(request=request, template_name='success.html', context={'logout': 'pessoa'})

def redireciona_sucesso(request):
    session_id = request.GET.get('session_id')
    if session_id:
        sessao = stripe.checkout.Session.retrieve(session_id)
        valor = sessao.amount_total / 100
        Doacao.objects.create(id_pessoa = request.session['id_pessoa'], valor_doacao = valor)
        pessoa = Pessoa.objects.get(id=request.session['id_pessoa'])
        pessoa.valor_total_doado_pessoa += valor
        pessoa.save()
    return redirect(reverse('pessoa_doacao_sucesso_rendeniza'))

def redireciona_cancelado(request):
    return render(request=request, template_name='cancel.html')