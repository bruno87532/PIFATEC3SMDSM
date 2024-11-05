from django.urls import path
from empresa.views import EmpresaCadastro, EmpresaDoacao, EmpresaDoacaoLista, EmpresaDoacaoLocaliza, EmpresaDoacaoMinha, gera_pdf
urlpatternscad = [
    path('', EmpresaCadastro.as_view(), name='empresapostcad'),
    path('<int:etapa>/', EmpresaCadastro.as_view(), name='empresagetcad')
]
urlpatternsdoacao = [
    path('', EmpresaDoacao.as_view(), name='empresa_doacao'),
    path('lista/<int:numero_pagina>/', EmpresaDoacaoLista.as_view(), name='empresa_doacao_lista'),
    path('empresa/<int:numero_pagina>/', EmpresaDoacaoLocaliza.as_view(), name='empresa_doacao_localiza'),
    path('minha/<int:numero_pagina>', EmpresaDoacaoMinha.as_view(), name='empresa_doacao_minha'),
    path('gera/<int:id>', gera_pdf, name='gera_pdf')
]