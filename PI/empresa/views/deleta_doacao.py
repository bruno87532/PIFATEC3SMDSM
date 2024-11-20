from django.views import View
from empresa.models import Doacao
from django.shortcuts import redirect
from django.urls import reverse

class DeletaDoacao(View):
    def dispatch(self, request, *args, **kwargs):
        if 'id_empresa' not in request.session:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, id, numero_pagina):
        doacao = Doacao.objects.get(id=id)
        if doacao.disponivel_produto:
            Doacao.objects.get(id=id).delete()
        return redirect(reverse('empresa_doacao_minha', kwargs={'numero_pagina': numero_pagina}))