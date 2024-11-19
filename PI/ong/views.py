from django.shortcuts import render, redirect
from ong.forms import OngFormUm, OngFormDois, OngFormTres, OngCompleta
from django.views import View
from empresa.models import Empresa, Doacao
from ong.models import Ong, DoacaoRecebida
from django.core.paginator import Paginator

class OngCadastro(View):
    def __init__(self, *args, **kwargs):
        self.templates = {
            1: ['cadastro_um_ong.html', OngFormUm],
            2: ['cadastro_dois_ong.html', OngFormDois],
            3: ['cadastro_tres_ong.html', OngFormTres]
        }
        super().__init__(*args, **kwargs)
    def get(self, request, etapa):
        template = self.templates[etapa][0]
        form = self.templates[etapa][1]()
        if etapa > 1 and not f'etapa{etapa-1}' in request.session:
            return redirect('onggetcad', etapa=1)
        return render(request=request, template_name=template, context={'form': form}) 
    def post(self, request):
        chave = 1 if request.POST.get('etapa1', '') else (2 if request.POST.get('etapa2', '') else 3)
        form = self.templates[chave][1](request.POST)
        if form.is_valid():
            if chave == 1:
                request.session['ong'] = form.cleaned_data
                request.session['etapa1'] = True
            elif chave == 2:
                request.session['ong'] = request.session['ong'] | form.cleaned_data
                request.session['etapa2'] = True
            elif chave == 3:
                form_completo = OngCompleta(request.session['ong'] | form.cleaned_data)
                ong = form_completo.save(commit=False)
                ong.set_senha(form_completo.cleaned_data['senha_login'])
                ong.save()
                return redirect('login')
            request.session.modified = True
            return redirect('onggetcad', etapa = chave + 1)
        else:
            erros_chave = ['nome_erro', 'cnpj_erro', 'cnpj_existe', 'email_login_erro', 'senha_login_erro', 'cep_erro', 'nome_representante_erro', 'telefone_representante_erro', 'cpf_representante_erro']
            erros_valor = ['Nome inválido', 'CNPJ inválido', 'CNPJ já cadastrado', 'Email já cadastrado', 'Senha inválida', 'CEP inválido', 'Nome do representante inválido',  'Telefone do representante inválido', 'CPF do representante inválido']
            lista_erros = list(form.errors.values())
            lista_erros = [i for erro in lista_erros for i in erro]
            lista_contexto = []
            for c, v in zip(erros_chave, erros_valor):
                if v in lista_erros:
                    lista_contexto.append({c: v})
            return render(request=request, template_name=self.templates[chave][0], context={'form': form, 'erro': lista_contexto})
    
class OngDistribuicao(View):
    def get(self, request, numero_pagina):
        empresas = {empresa.id: empresa.nome for empresa in Empresa.objects.all()}
        ongs = Ong.objects.all().values('id', 'nome')
        nomes = {i['id']: i['nome'] for i in ongs}
        print(nomes)
        doacoes = Doacao.objects.filter(disponivel_produto__in=[True]).values('id_empresa', 'id', 'nome_produto', 'quantidade_produto', 'unidade_medida_produto', 'data_doado_produto', 'disponivel_produto') 
        lista_contexto = [{
            'id': i['id'],
            'nome_empresa': empresas.get(int(i['id_empresa'])),
            'nome_produto': i['nome_produto'],
            'quantidade_produto': i['quantidade_produto'],
            'unidade_medida_produto': i['unidade_medida_produto'],
            'data_doado_produto': i['data_doado_produto'],
            'disponivel_produto': i['disponivel_produto'],
        } for i in doacoes]
        doacao_paginada = Paginator(lista_contexto, 10)
        pagina = doacao_paginada.get_page(numero_pagina)
        return render(request=request, template_name='distribui_doacao_ong.html', context={'doacoes': pagina, 'ongs': nomes})
    def post(self, request, numero_pagina):
        dicionario = {int(i): int(j) for i, e in request.POST.items() for j in e if i.isdigit()} # Primeiro o id da doaçao, segundo o da ong que vai receber
        for i, e in dicionario.items():
            doacao = Doacao.objects.get(id=i)
            doacao.disponivel_produto = False
            doacao.save()
            ong = Ong.objects.get(id=e)
            doacao_recebida = DoacaoRecebida(
                id_empresa = i,
                id_ong = ong.id,
                nome_produto = doacao.nome_produto,
                descricao_produto = doacao.descricao_produto,
                quantidade_produto = doacao.quantidade_produto,
                unidade_medida_produto = doacao.unidade_medida_produto,
                categoria_produto = doacao.categoria_produto,
                data_doado_produto = doacao.data_doado_produto
            )
            doacao_recebida.save()
        return redirect('distribuicao_ong', numero_pagina=numero_pagina)