from django.shortcuts import render
from django.views import View

class Login(View):
    def get(self, request):
        return render(request=request, template_name='login.html')
