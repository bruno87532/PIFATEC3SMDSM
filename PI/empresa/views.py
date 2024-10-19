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
            template = 'cadastro_dois.html'
            form = EmpresaFormDois()
        elif etapa == 3:
            template = 'cadastro_tres.html'
            form = EmpresaFormTres()
        return render(request=request, template_name=template, context={'form': form}) 
    def post(self, request):
        if request.POST.get('etapa1', ''):
            form = EmpresaFormUm(request.POST)
            if form.is_valid():
                request.session['empresa'] = request.POST
                request.session.modified = True
                print(request.session['empresa'])
                return redirect('empresagetcad', etapa = 2)
        elif request.POST.get('etapa2', ''):
            form = EmpresaFormDois(request.POST)
            if form.is_valid():
                request.session['empresa'] = request.session['empresa'] | request.POST
                request.session.modified = True
                print(request.session['empresa'])
                return redirect('empresagetcad', etapa = 3)
        elif request.POST.get('etapa3', ''):
            form = EmpresaFormTres(request.POST)
            if form.is_valid():
                request.session['empresa'] = request.session['empresa'] | request.POST
                print(request.session['empresa'])
                form_completo = EmpresaCompleta(request.session['empresa'])
                request.session['empresa'].pop('etapa1')
                request.session['empresa'].pop('etapa2')
                request.session['empresa'].pop('etapa3')
                form_completo.save()
                return render(request=request, template_name='login_empresa.html')
            else:
                print(f'teste: {form.errors}')
        
class EmpresaLogin(View):
    def get(self, request):
        return render(request=request, template_name='login.html')