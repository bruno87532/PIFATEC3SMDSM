from django.shortcuts import render
from empresa.forms import EmpresaForm
from rest_framework.views import APIView
from django.http import JsonResponse

# Create your views here.

class Empresa(APIView):
    def get(self, request):
        form = EmpresaForm()
        return render(request=request, template_name='cadastro_um.html', context={'form': form})    
    def post(self, request):
        return JsonResponse(request.data)
