from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class Home(APIView):
    def get(self, request):
        login = {
            'id_empresa': 'empresa',
            'id_ong': 'ong',
            'id_pessoa': 'pessoa'
        }
        for k, v in login.items():
            if request.session.get(k):
                return render(request=request, template_name='index.html', context={'logout': v})
        return render(request=request, template_name='index.html') 

class Erro(APIView):
    def get(self, request):
        return render(request=request, template_name='erro.html')