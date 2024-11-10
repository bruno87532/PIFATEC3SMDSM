from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class Home(APIView):
    def get(self, request):
        if request.session.get('id_empresa') or request.session.get('id_pessoa') or request.session.get('id_ong'):
            return render(request=request, template_name='index.html', context={'logout': True})
        return render(request=request, template_name='index.html') 
