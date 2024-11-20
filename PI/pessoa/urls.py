from django.urls import path
from pessoa.views.cadastro import PessoaCadastro
from pessoa.views.realiza_pagamento import PessoaDoacao, redireciona_cancelado, redireciona_sucesso, rendeniza_sucesso
from pessoa.views.pagamento_proprio import PessoaPagamentoProprio
from pessoa.views.pagamento_lista import PessoaPagamentoLista
from pessoa.views.pagamento_ranking import PessoaPagamentoRanking
urlpatternscad = [
    path('', PessoaCadastro.as_view(), name='pessoa'),
]

urlpatternsdoacao = [
    path('', PessoaDoacao.as_view(), name='pessoa_doacao'),
    path('sucessoredireciona', redireciona_sucesso, name='pessoa_doacao_sucesso'),
    path('sucesso', rendeniza_sucesso, name='pessoa_doacao_sucesso_rendeniza'),
    path('cancelado', redireciona_cancelado, name='pessoa_doacao_cancelado'),
    path('minha/<int:numero_pagina>', PessoaPagamentoProprio.as_view(), name='pessoa_pagamento_proprio'),
    path('lista/<int:numero_pagina>', PessoaPagamentoLista.as_view(), name='pessoa_pagamento_lista'),
    path('ranking/<int:numero_pagina>', PessoaPagamentoRanking.as_view(), name='pessoa_pagamento_ranking')
]