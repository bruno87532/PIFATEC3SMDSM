from datetime import timedelta

class GeraContexto():

    @classmethod
    def ContextoEmpresa(self, doacoes, empresas, ong = None):
        lista_contexto = []
        lista_contexto = [
            {
                'id': i['id'],
                'nome_empresa': empresas.get(int(i['id_empresa'])) if type(empresas) is dict else empresas.nome,
                'nome_produto': i['nome_produto'],
                'quantidade_produto': i['quantidade_produto'],
                'unidade_medida_produto': i['unidade_medida_produto'],
                'data_doado_produto': i['data_doado_produto'] - timedelta(hours=3),
                'disponivel_produto': i['disponivel_produto'] if not ong else '',
            }
            for i in doacoes
        ]
        return lista_contexto
    