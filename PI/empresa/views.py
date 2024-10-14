from django.shortcuts import render
from empresa.forms import EmpresaFormUm, EmpresaFormDois, EmpresaFormTres
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView
from empresa.serializers import EmpresaSerializer

# Create your views here.

class EmpresaCadastro(ListCreateAPIView):
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
        try:
            etapa = request.data.get('etapa')
            if etapa == 1:
                form = EmpresaFormUm(request.data)

            elif etapa == 2:
                form = EmpresaFormDois(request.data)

            elif etapa == 3:
                form = EmpresaFormTres(request.data)

            if form.is_valid():
                if not request.session.get('dados_empresa', ''):
                    request.session['dados_empresa'] = form.cleaned_data
                else:
                    request.session['dados_empresa'].update(form.cleaned_data)
                request.session.modified = True
                if etapa == 3:
                    serializer = EmpresaSerializer(data = form.cleaned_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        ...
                        print(serializer.errors)
                        ## Devo tratar aqui
                print(request.session['dados_empresa'])
                return JsonResponse({'status': 'sucesso'}, status=201)
        except Exception as e:
            return JsonResponse({
                'erro': str(e)
            }, status = 500)
        
        ## POSTERIORMENTE REFATORE ESTE CÓDIGO PARA MELHORAR
class EmpresaLogin(ListCreateAPIView):
    def get(self, request):
        return render(request=request, template_name='login.html')