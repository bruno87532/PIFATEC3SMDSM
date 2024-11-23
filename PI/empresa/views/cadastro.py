from django.shortcuts import render, redirect
from empresa.forms import EmpresaFormUm, EmpresaFormDois, EmpresaFormTres, EmpresaCompleta
from django.views import View

class EmpresaCadastro(View):
    def __init__(self, *args, **kwargs):
        self.templates = {
            1: ['cadastro_um.html', EmpresaFormUm],
            2: ['cadastro_dois.html', EmpresaFormDois],
            3: ['cadastro_tres.html', EmpresaFormTres]
        }
        super().__init__(*args, **kwargs)
    def get(self, request, etapa):
        template = self.templates[etapa][0]
        form = self.templates[etapa][1]()
        if etapa > 1 and not f'etapa{etapa-1}' in request.session:
            return redirect('empresagetcad', etapa=1)
        return render(request=request, template_name=template, context={'form': form}) 
    def post(self, request):
        chave = 1 if request.POST.get('etapa1', '') else (2 if request.POST.get('etapa2', '') else (3 if request.POST.get('etapa3', '') else ''))
        if chave == '':
            return redirect('home')
        form = self.templates[chave][1](request.POST)
        if form.is_valid():
            if chave == 1:
                request.session['empresa'] = form.cleaned_data
                request.session['etapa1'] = True
            elif chave == 2:
                request.session['empresa'] = request.session['empresa'] | form.cleaned_data
                request.session['etapa2'] = True
            elif chave == 3:
                form_completo = EmpresaCompleta(request.session['empresa'] | form.cleaned_data)
                empresa = form_completo.save(commit=False)
                empresa.set_senha(form_completo.cleaned_data['senha_login'])
                empresa.save()
                return redirect('login')
            request.session.modified = True
            return redirect('empresagetcad', etapa = chave + 1)
        else:
            return render(request=request, template_name=self.templates[chave][0], context={'form': form}, status=400)