from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from pessoa.forms import PessoaForm
from django.http import JsonResponse
from pessoa.forms import PessoaForm
from pessoa.serializers import PessoaSerializer

# Create your views here.

class PessoaCadastro(ListCreateAPIView):
    def get(self, request):
        form = PessoaForm()
        return render(request=request, template_name='cadastro.html',  context={'form': form})
    def post(self, request):
        try:
            form = PessoaForm(request.data)
            if form.is_valid():
                serializer = PessoaSerializer(data = form.cleaned_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'status': 'sucesso'}, status=201)
                else:
                    form = PessoaForm(request.data)
                    lista_erro = list(serializer.errors.keys())
                    lista_contexto = []
                    if 'cpf_pessoa' in lista_erro:
                        cpf_erro = {'cpf_erro': 'CPF inválido'}
                        lista_contexto.append(cpf_erro)
                    if 'data_nascimento_pessoa' in lista_erro:
                        data_nascimento_erro = {'data_nascimento_erro': 'Data de nascimento inválida'}
                        lista_contexto.append(data_nascimento_erro)
                    return render(request=request, template_name='cadastro.html', context={'form': form, 'erro': lista_contexto})
            else: 
                # Tratar aqui
                ...
        except Exception as e:
            return JsonResponse({
                'erro': str(e)
            }, status = 500)

class PessoaLogin(ListCreateAPIView):
    def get(self, request):
        return render(request=request, template_name='login.html')