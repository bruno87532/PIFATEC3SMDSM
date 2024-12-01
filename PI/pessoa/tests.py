from django.test import TestCase
from datetime import date
from django.urls import reverse
from pessoa.models import Pessoa, Doacao

class BaseTestCase(TestCase):
    def setUp(self):
        self.dados = {
            'nome_pessoa': 'Bruno Henrique Guinerio', 
            'cpf_pessoa': '08883681002', 
            'email_login_pessoa': 'teste@gmail.com',
            'senha_login_pessoa': '123456789',
            'data_nascimento_pessoa': date(2003, 4, 12), 
            'telefone_pessoa': '19982869853'
        }
        return super().setUp()
    def nao_contem_conteudo(self, resposta, conteudos, status):
        for conteudo in conteudos:
            self.assertNotContains(resposta, conteudo, status_code=status)
    def contem_conteudo(self, resposta, conteudos, status):
        for conteudo in conteudos:
            self.assertContains(resposta, conteudo, status_code=status)
    def cria_pessoa(self):
        self.client.post(reverse('pessoa'), self.dados)

    def login_pessoa(self):
        self.cria_pessoa()
        self.login = {
            'email': self.dados['email_login_pessoa'],
            'senha': self.dados['senha_login_pessoa']
        }
        self.client.post(reverse('login'), self.login)

class cadastra_dados_correto_pessoa(BaseTestCase):
    def test_cadastro(self):
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertTemplateNotUsed(resposta, 'cadastro.html')
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('login'))

class cadatra_dados_errado_pessoa(BaseTestCase):
    def test_cadastro_cpf_invalido(self):
        self.dados['cpf_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.contem_conteudo(resposta, ['CPF inválido'], 400)
        self.nao_contem_conteudo(resposta, ['Nome inválido', 'É necessário ser maior de idade', 'Senha inválida', 'Número de telefone inválido'], 400)
    def test_cadastro_nome_invalido(self):
        self.dados['nome_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.contem_conteudo(resposta, ['Nome inválido'], 400)
        self.nao_contem_conteudo(resposta, ['CPF inválido', 'É necessário ser maior de idade', 'Senha inválida', 'Número de telefone inválido'], 400)
    def test_cadastro_data_nascimento_invalida(self):
        self.dados['data_nascimento_pessoa'] = date(2024, 4, 12)
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.contem_conteudo(resposta, ['É necessário ser maior de idade'], 400)
        self.nao_contem_conteudo(resposta, ['CPF inválido', 'Senha inválida', 'Número de telefone inválido', 'Nome inválido'], 400)
    def test_cadastro_telefone_invalido(self):
        self.dados['telefone_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.contem_conteudo(resposta, ['Número de telefone inválido'], 400)
        self.nao_contem_conteudo(resposta, ['CPF inválido', 'É necessário ser maior de idade', 'Senha inválida', 'Nome inválido'], 400)
    def test_cadastro_senha_invalida(self):
        self.dados['senha_login_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.assertTemplateNotUsed(resposta, 'login.html')
        self.assertTemplateUsed(resposta, 'cadastro.html')
        self.contem_conteudo(resposta, ['Senha inválida'], 400)
        self.nao_contem_conteudo(resposta, ['É necessário ser maior de idade', 'CPF inválido', 'Número de telefone inválido', 'Nome inválido'], 400)
    def test_cadastro_senha_telefone_data_nome_cpf(self):
        self.dados['cpf_pessoa'] = '123'
        self.dados['nome_pessoa'] = '123'
        self.dados['data_nascimento_pessoa'] = date(2024, 4, 12)
        self.dados['telefone_pessoa'] = '123'
        self.dados['senha_login_pessoa'] = '123'
        resposta = self.client.post(reverse('pessoa'), self.dados)
        self.contem_conteudo(resposta, ['Senha inválida', 'É necessário ser maior de idade', 'CPF inválido', 'Número de telefone inválido', 'Nome inválido'], 400)

class GET_redireciona_pagamento_realiza(BaseTestCase):
    def test_redireciona_sem_login(self):
        resposta = self.client.get(reverse('pessoa_doacao'))
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('login'))
    def test_redireciona_com_login(self):
        self.login_pessoa()
        resposta = self.client.get(reverse('pessoa_doacao'))
        self.assertTemplateUsed(resposta, 'pix.html')

class realiza_pagamento(BaseTestCase):
    def post_pagamento_retorna_json(self):
        self.dados = {'valor': '50'}
        resposta = self.client.post(reverse('pessoa_doacao'))
        self.assertIn('application/pdf', resposta['Content-Type'])
    
class rendeniza_ranking_pagamento(BaseTestCase):
    def test_ranking_pagamento(self):
        Pessoa.objects.create(nome_pessoa = 'Bruno', valor_total_doado_pessoa = '2000')
        Pessoa.objects.create(nome_pessoa = 'Gabriel', valor_total_doado_pessoa = '5000')
        resposta = self.client.get(reverse('pessoa_pagamento_ranking'))
        self.assertTemplateUsed(resposta, 'ranking_pagamento.html')
        self.assertContains(resposta, '<tr><td>1</td><td>Gabriel</td><td>5000.0</td></tr><tr><td>2</td><td>Bruno</td><td>2000.0</td></tr>', html=True)


class visualiza_pagamento_proprio(BaseTestCase):
    def test_meu_pagamento(self):
        self.login_pessoa()
        Doacao.objects.create(id_pessoa = Pessoa.objects.last().id, valor_doacao = '50', data_doado = date.today())
        Doacao.objects.create(id_pessoa = Pessoa.objects.last().id - 1, valor_doacao = '30', data_doado = date.today())
        resposta = self.client.get(reverse('pessoa_pagamento_proprio', kwargs={'numero_pagina': '1'}))
        self.assertTemplateUsed(resposta, 'visualiza_pagamento_meu.html')
        self.assertContains(resposta, '50')
        self.assertNotContains(resposta, '30')

class GET_redireciona_pagamento_proprio(BaseTestCase):
    def test_redireciona_sem_login(self):
        resposta = self.client.get(reverse('pessoa_pagamento_proprio', kwargs={'numero_pagina': '1'}))
        self.assertEqual(302, resposta.status_code)
        self.assertRedirects(resposta, reverse('login'))
    def test_redireciona_com_login(self):
        self.login_pessoa()
        resposta = self.client.get(reverse('pessoa_pagamento_proprio', kwargs={'numero_pagina': '1'}))
        self.assertTemplateUsed(resposta, 'visualiza_pagamento_meu.html')

class visualiza_pagamento_lista(BaseTestCase):
    def visualiza_todos_pagamentos(self):
        self.login_pessoa()
        Doacao.objects.create(id_pessoa = Pessoa.objects.last().id, data_doado = date.today(), valor_doacao = '50')
        self.dados['nome_pessoa'] = 'Christian Santos Rocha'
        self.dados['email_login_pessoa'] = 'teste2@gmail.com'
        self.login_pessoa()
        Doacao.objects.create(id_pessoa = Pessoa.objects.last().id, data_doado = date.today(), valor_doacao = '30')
        resposta = self.client.get(reverse('pessoa_pagamento_lista', kwargs={'numero_pagina': '1'}))
        self.assertContains(resposta, '30')
        self.assertContains(resposta, 'Christian Santos Rocha')
        self.assertContains(resposta, 'Bruno Henrique Guinerio')
        self.assertContains(resposta, '50')

