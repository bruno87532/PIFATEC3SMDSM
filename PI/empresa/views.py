from django.shortcuts import render
from empresa.forms import EmpresaForm
from rest_framework.views import APIView
from django.http import JsonResponse

# Create your views here.

class EmpresaCadastro(APIView):
    def get(self, request, etapa):
        if etapa == 1:
            template = 'cadastro_um.html'
        elif etapa == 2:
            template = 'cadastro_dois.html'
        elif etapa == 3:
            template = 'cadastro_tres.html'
        form = EmpresaForm()
        return render(request=request, template_name=template, context={'form': form})    
    def post(self, request):
        try:
            request.session['dados_empresa'] =  request.data
            print(request.session['dados_empresa'])
            return JsonResponse({
                'status': 'sucesso',
            }, status = 201)
        except Exception as e:
            return JsonResponse({
                'erro': str(e)
            }, status = 500)
class EmpresaLogin(APIView):
    def get(self, request):
        return render(request=request, template_name='login.html')