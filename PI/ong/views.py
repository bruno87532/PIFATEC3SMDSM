from django.shortcuts import render, redirect
from ong.forms import OngFormUm, OngFormDois, OngFormTres, OngCompleta
from django.views import View

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
        print(lista_contexto)
        return render(request=request, template_name=self.templates[chave][0], context={'form': form, 'erro': lista_contexto})