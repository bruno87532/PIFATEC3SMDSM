from django.shortcuts import render, redirect
from django.views import View
from empresa.models import Empresa
from pessoa.models import Pessoa
from ong.models import Ong
from django.contrib.auth import logout

class Login(View):
    def get(self, request):
        request.session.flush()
        return render(request=request, template_name='login.html')
    def post(self, request):
        email = request.POST['email']
        senha = request.POST['senha']
        autenticado = False
        try:
            empresa = Empresa.objects.get(email_login=email)
            if empresa.verifica_senha(senha):
                request.session['id_empresa'] = empresa.id
                autenticado = True    
        except Empresa.DoesNotExist:
            pass
        try:
            pessoa = Pessoa.objects.get(email_login_pessoa=email)
            if pessoa.verifica_senha(senha):
                request.session['id_pessoa'] = pessoa.id
                autenticado = True
        except Pessoa.DoesNotExist:
            pass
        try:
            ong = Ong.objects.get(email_login=email)
            if ong.verifica_senha(senha):
                request.session['id_ong'] = ong.id
                autenticado = True
        except Ong.DoesNotExist:
            pass
        if not autenticado:
            return render(request=request, template_name='login.html', context={'email': email}, status=400)
        return redirect('home')
class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect('home')