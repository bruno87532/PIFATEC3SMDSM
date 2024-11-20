from django.urls import path
from empresa.views.cadastro import EmpresaCadastro
from empresa.views.doacao import EmpresaDoacao
from empresa.views.lista_doacao import EmpresaDoacaoLista
from empresa.views.localiza_doacao import EmpresaDoacaoLocaliza
from empresa.views.minha_doacao import EmpresaDoacaoMinha
from empresa.views.gera_pdf import GeraPdfView
from empresa.views.deleta_doacao import DeletaDoacao

urlpatternscad = [
    path('', EmpresaCadastro.as_view(), name='empresapostcad'),
    path('<int:etapa>/', EmpresaCadastro.as_view(), name='empresagetcad')
]
urlpatternsdoacao = [
    path('', EmpresaDoacao.as_view(), name='empresa_doacao'),
    path('lista/<int:numero_pagina>/', EmpresaDoacaoLista.as_view(), name='empresa_doacao_lista'),
    path('empresa/<int:numero_pagina>/', EmpresaDoacaoLocaliza.as_view(), name='empresa_doacao_localiza'),
    path('minha/<int:numero_pagina>', EmpresaDoacaoMinha.as_view(), name='empresa_doacao_minha'),
    path('gera/<int:id>', GeraPdfView.as_view(), name='gera_pdf'),
    path('deletar/<int:id>/<int:numero_pagina>', DeletaDoacao.as_view(),name='deleta_doacao')
]