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
            return render(request=request, template_name='cadastro.html', context={'form': form}, status=400)