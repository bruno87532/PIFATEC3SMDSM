from django.test import TestCase
from django.urls import reverse
from empresa.models import Empresa, Doacao
from datetime import datetime, timedelta

# Create your tests here.

class BaseTestCase(TestCase):
    def setUp(self):
        self.dados_etapa_1 = {
            'nome': 'Coca-Cola',
            'cnpj': '45997418002601',
            'email_login': 'cocacolacontato@gmail.com',
            'senha_login': '123456789',
            'tipo_empresa': 'sociedade de capital fechado',
            'etapa1': '1'
        }
        self.dados_etapa_2 = {
            'cep': '13610827', 
            'estado': 'SP', 
            'cidade': 'Leme', 
            'bairro': 'Jardim do Sol', 
            'rua': 'Maria Fercem', 
            'numero': '232',
            'complemento': 'bloco 8 ap 104',
            'etapa2': '2'
        }
        self.dados_etapa_3 = {
            'nome_representante': 'Bruno Henrique Guinerio',
            'cpf_representante': '85700565080',
            'telefone_representante': '19982869853',
            'email_representante': 'brunoguinerio@gmail.com',
            'etapa3': '3'
        }
        self.dados_doacao = {
            'nome_produto': 'Feijão',
            'descricao_produto': 'Feijão broto legal 1kg',
            'quantidade_produto': '5',
            'unidade_medida_produto': 'unidade',
            'categoria_produto': 'mercearia'
        }
        return super().setUp()
    def nao_contem_conteudo(self, resposta, conteudos, status):
        for conteudo in conteudos:
            self.assertNotContains(resposta, conteudo, status_code=status)
    def contem_conteudo(self, resposta, conteudos, status):
        for conteudo in conteudos:
            self.assertContains(resposta, conteudo, status_code=status)
    def cria_empresa(self):
        self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.client.post(reverse('empresapostcad'), self.dados_etapa_2)
        self.client.post(reverse('empresapostcad'), self.dados_etapa_3) 

    def login_empresa(self):
        self.cria_empresa()
        self.login = {
            'email': self.dados_etapa_1['email_login'],
            'senha': self.dados_etapa_1['senha_login']
        }
        self.client.post(reverse('login'), self.login)


class GET_redireciona_correto_cadastro(BaseTestCase):
    def test_rota_1(self):
        resposta = self.client.get(reverse('empresagetcad', kwargs={'etapa': 1}))
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
    def test_rota_2_redireciona_1(self):
        resposta = self.client.get(reverse('empresagetcad', kwargs={'etapa': 2}), follow=True)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
    def test_rota_2_redireciona_1(self):
        resposta = self.client.get(reverse('empresagetcad', kwargs={'etapa': 3}), follow=True)
        self.assertTemplateNotUsed(resposta, 'cadastro_tres.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')

class cadastra_dados_correto_cadastro(BaseTestCase):
    def test_cadastro(self):
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('empresagetcad', kwargs={'etapa': 2}))
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_2)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('empresagetcad', kwargs={'etapa': 3}))
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_3)
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))
        self.assertEqual(Empresa.objects.count(), 1)

class cadastra_dados_repetidos_cadastro(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cria_empresa()
    def test_dado_cnpj_repetido(self):
        self.dados_etapa_1['email_login'] = 'teste@gmail.com'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.nao_contem_conteudo(resposta, ['Email já cadastrado'], 400)
        self.contem_conteudo(resposta, ['CNPJ já cadastrado'], 400)
    def test_dado_email_repetido(self):
        self.dados_etapa_1['cnpj'] = '09606174000177'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.contem_conteudo(resposta, ['Email já cadastrado'], 400)
        self.nao_contem_conteudo(resposta, ['CNPJ já cadastrado'], 400)
    def test_dado_cnpj_email_repetido(self):
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.contem_conteudo(resposta, ['Email já cadastrado', 'CNPJ já cadastrado'], 400)

class cadastra_dados_vazio_cadastro(BaseTestCase):
    def test_dados_vazio_etapa_1(self):
        for i in self.dados_etapa_1:
            self.dados_etapa_1[i] = ''
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('home'))
    def test_dados_vazio_etapa_2(self):
        self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        for i in self.dados_etapa_2:
            self.dados_etapa_2[i] = ''
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_2)
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('home'))
    def test_dados_vazio_etapa_3(self):
        self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.client.post(reverse('empresapostcad'), self.dados_etapa_2)
        for i in self.dados_etapa_3:
            self.dados_etapa_3[i] = ''        
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_3)
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('home'))

class cadastra_dados_errado_etapa_1_cadastro(BaseTestCase):
    def test_errado_etapa_1_cnpj(self):
        self.dados_etapa_1['cnpj'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.contem_conteudo(resposta, ['CNPJ inválido'], 400)
        self.nao_contem_conteudo(resposta, ['Senha inválida'], 400)
    def test_errado_etapa_1_senha(self):
        self.dados_etapa_1['senha_login'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.nao_contem_conteudo(resposta, ['CNPJ inválido'], 400)
        self.contem_conteudo(resposta, ['Senha inválida'], 400)
    def test_errado_etapa_1_cnpj_senha(self):
        self.dados_etapa_1['senha_login'] = '123'
        self.dados_etapa_1['cnpj'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.assertTemplateNotUsed(resposta, 'cadastro_dois.html')
        self.assertTemplateUsed(resposta, 'cadastro_um.html')
        self.contem_conteudo(resposta, ['Senha inválida', 'CNPJ inválido'], 400)
 
class cadastra_dados_errado_etapa_2_cadastro(BaseTestCase):
    def test_errado_etapa_2_cep(self):
        self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.dados_etapa_2['cep'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_2)
        self.assertTemplateNotUsed('cadastro_tres.html')               
        self.assertTemplateUsed('cadastro_dois.html')
        self.contem_conteudo(resposta, ['CEP inválido'], 400) 

class cadastra_dados_errado_etapa_3_cadastro(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('empresapostcad'), self.dados_etapa_1)
        self.client.post(reverse('empresapostcad'), self.dados_etapa_2)
    def test_errado_etapa_3_cpf_representante(self):
        self.dados_etapa_3['cpf_representante'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_3)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.contem_conteudo(resposta, ['CPF do representante inválido'], 400)
        self.nao_contem_conteudo(resposta, ['Telefone do representante inválido', 'Nome do representante inválido'], 400)
    def test_errado_etapa_3_nome_representante(self):
        self.dados_etapa_3['nome_representante'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_3)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.contem_conteudo(resposta, ['Nome do representante inválido'], 400)
        self.nao_contem_conteudo(resposta, ['CPF do representante inválido', 'Telefone do representante inválido'], 400)
    def test_errado_etapa_3_telefone(self):
        self.dados_etapa_3['telefone_representante'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_3)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.nao_contem_conteudo(resposta, ['CPF do representante inválido', 'Nome do representante inválido'], 400)
        self.contem_conteudo(resposta, ['Telefone do representante inválido'], 400)
    def test_errado_etapa_3_cpf_telefone_nome_representante(self):
        self.dados_etapa_3['telefone_representante'] = '123'
        self.dados_etapa_3['nome_representante'] = '123'
        self.dados_etapa_3['cpf_representante'] = '123'
        resposta = self.client.post(reverse('empresapostcad'), self.dados_etapa_3)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro_tres.html')
        self.contem_conteudo(resposta, ['CPF do representante inválido', 'Nome do representante inválido', 'Telefone do representante inválido'], 400)

class GET_redireciona_correto_doacao(BaseTestCase):
    def test_redireciona_sem_login(self):
        resposta = self.client.get(reverse('empresa_doacao'), follow=True)
        self.assertTemplateNotUsed(resposta, 'doacao_empresa.html')
        self.assertTemplateUsed(resposta, 'login.html')
    def test_redireciona_com_login(self):
        self.login_empresa()
        resposta = self.client.get(reverse('empresa_doacao'), follow=True)
        self.assertTemplateUsed(resposta, 'doacao_empresa.html')
        self.assertTemplateNotUsed(resposta, 'login.html')

class cadastra_dados_errado_doacao(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login_empresa()
    def test_errado_quantidade(self):
        self.dados_doacao['quantidade_produto'] = '5.5.5'
        self.dados_doacao['unidade_medida_produto'] = 'gramas'
        resposta = self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.contem_conteudo(resposta, ['Quantidade inválida'], 400)
        self.nao_contem_conteudo(resposta, ['O valor deve ser inteiro para medidas unitária'], 400)
    def test_errado_unidade(self):
        self.dados_doacao['unidade_medida_produto'] = 'unidade'
        self.dados_doacao['quantidade_produto'] = '5.5'
        resposta = self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.contem_conteudo(resposta, ['O valor deve ser inteiro para medidas unitária'], 400)
        self.nao_contem_conteudo(resposta, ['Quantidade inválida'], 400)
    def test_errado_quantidade_unidade(self):
        self.dados_doacao['unidade_medida_produto'] = 'unidade'
        self.dados_doacao['quantidade_produto'] = '5,5,5'
        resposta = self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.contem_conteudo(resposta, ['O valor deve ser inteiro para medidas unitária', 'Quantidade inválida'], 400)

class cadastra_dados_correto_doacao(BaseTestCase):
    def test_doacao(self):
        self.login_empresa()
        resposta = self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.assertEqual(Doacao.objects.count(), 1)

class GET_redireciona_correto_minha_doacao(BaseTestCase):
    def test_redireciona_sem_login(self):
        resposta = self.client.get(reverse('empresa_doacao_minha', kwargs={'numero_pagina': 1}), follow=True)
        self.assertTemplateNotUsed(resposta, 'visualiza_doacao_minha.html')
        self.assertTemplateUsed(resposta, 'login.html')
    def test_redireciona_com_login(self):
        self.login_empresa()
        resposta = self.client.get(reverse('empresa_doacao_minha', kwargs={'numero_pagina': 1}), follow=True)
        self.assertTemplateUsed(resposta, 'visualiza_doacao_minha.html')
        self.assertTemplateNotUsed(resposta, 'login.html')

class mostra_minha_doacao(BaseTestCase):
    def test_mostra_doacao(self):
        self.login_empresa()
        resposta = self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        resposta = self.client.get(reverse('empresa_doacao_minha', kwargs={'numero_pagina': 1}), follow=True)
        self.contem_conteudo(resposta, ['Feijão', 'Coca-Cola', 'unidade', '5', (datetime.now() - timedelta(hours=3)).strftime("%d/%m/%Y")], 200)
        self.assertContains(resposta, (datetime.now() - timedelta(hours=3)).strftime("%d/%m/%Y"))
        doacao = Doacao.objects.last()
        # self.assertContains(resposta, '<td><a href="/doacao/gera/16" target="_blank">Certificado da doação</a></td>', html=True)

class doacao_todas_empresas(BaseTestCase):
    def test_todas_doacoes(self):
        self.login_empresa()
        self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.dados_etapa_1['nome'] = 'Oreo'
        self.dados_etapa_1['cnpj'] = '31340025000168'
        self.dados_etapa_1['email_login'] = 'oreocontato@gmail.com'
        self.login_empresa()
        self.dados_doacao['nome_produto'] = 'Bolacha Oreo'
        self.dados_doacao['quantidade_produto'] = '5000'
        self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.dados_etapa_1['nome'] = 'Perdigão'
        self.dados_etapa_1['cnpj'] = '89421903013561'
        self.dados_etapa_1['email_login'] = 'perdigaocontato@gmail.com'
        self.login_empresa()
        self.dados_doacao['nome_produto'] = 'Macarrão'
        self.dados_doacao['quantidade_produto'] = '50'
        for i in range(10):
            self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        doacao = Doacao.objects.first()
        doacao.disponivel_produto = False
        doacao.save()
        resposta = self.client.get(reverse('empresa_doacao_lista', kwargs={'numero_pagina': 1}))
        self.contem_conteudo(resposta, ['Oreo', 'Bolacha Oreo', '5000', 'Macarrão', '50', 'Feijão', '5', 'Disponível', 'Não disponível', 'Próxima página', 'Perdigão'], 200)
        self.nao_contem_conteudo(resposta, ['Página anterior'], 200)
        resposta = self.client.get(reverse('empresa_doacao_lista', kwargs={'numero_pagina': 2}))
        self.contem_conteudo(resposta, ['Macarrão', '50', 'Perdigão', 'Página anterior'], 200)
        self.nao_contem_conteudo(resposta, ['Próxima página'], 200)

class deleta_doacao(BaseTestCase):
    def test_get_deleta_doacao_sem_login(self):
        resposta = self.client.get(reverse('deleta_doacao', kwargs={'id': 1, 'numero_pagina': 1}))
        self.assertTemplateNotUsed(resposta, 'visualiza_doacao_minha.html')
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))
    def test_get_deleta_doacao_com_login(self):
        self.login_empresa()
        self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        doacao = Doacao.objects.last()
        resposta = self.client.get(reverse('deleta_doacao', kwargs={'id': 2, 'numero_pagina': 1}))
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('empresa_doacao_minha', kwargs={'numero_pagina': 1}))
        self.assertEqual(0, Doacao.objects.count())

class gera_pdf(BaseTestCase):
    def test_get_gera_pdf_sem_login(self):
        resposta = self.client.get(reverse('gera_pdf', kwargs={'id': 1}))
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))
    def test_get_gera_pdf_com_login(self):
        self.login_empresa()
        resposta = self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        doacao = Doacao.objects.last()
        resposta = self.client.get(reverse('gera_pdf', kwargs={'id': 15}))
        self.assertIn('application/pdf', resposta.headers['Content-Type'])

class localiza_doacao(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login_empresa()
        self.client.post(reverse('empresa_doacao'), self.dados_doacao)
        self.dados_etapa_1['nome'] = 'Oreo'
        self.dados_etapa_1['cnpj'] = '54345304000110'
        self.dados_etapa_1['email_login'] = 'oreocontato@gmail.com'
        self.dados_doacao['nome_produto'] = 'Bolacha'
        self.dados_doacao['quantidade_produto'] = '500'
        self.login_empresa()
        self.client.post(reverse('empresa_doacao'), self.dados_doacao)
    def test_localiza_docao_por_post_empresa_nao_existe(self):  
        self.dados_empresa = {'nome_empresa': 'facebook'}
        resposta = self.client.post(reverse('empresa_doacao_localiza', kwargs={'numero_pagina': '1'}), self.dados_empresa)
        self.contem_conteudo(resposta, ['Não encontrado nenhuma empresa com este nome'], 200)
    def test_localiza_doacao_por_post_empresa_existe(self):
        self.dados_empresa = {'nome_empresa': 'Coca-Cola'}
        resposta = self.client.post(reverse('empresa_doacao_localiza', kwargs={'numero_pagina': '1'}), self.dados_empresa)
        self.contem_conteudo(resposta, ['Coca-Cola', 'Feijão', 'unidade', 'Disponível'], 200)
        self.nao_contem_conteudo(resposta, ['Oreo', 'Bolacha', '500'], 200)
    def test_localiza_doacao_por_get_nao_existe(self):
        self.client.session['nome_empresa'] = 'facebook'
        self.client.session.save()
        resposta = self.client.get(reverse('empresa_doacao_localiza', kwargs={'numero_pagina': '1'}))
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('empresa_doacao_lista', kwargs={'numero_pagina': '1'}))